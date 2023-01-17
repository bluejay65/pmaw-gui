from pmaw import PushshiftAPIBase
from pmaw.types.exceptions import HTTPError, HTTPNotFoundError
from pmaw.Metadata import Metadata
from pmaw import Request
from pmawinterface.pmaw_output import PMAWOutput
from backend.constants import CRITICAL_MESSAGE
import logging
import requests
import json
import copy


log = logging.getLogger(__name__)


class PushshiftAPIBaseInterface(PushshiftAPIBase):
    
    def __init__(self, executor, output, main_thread, **kwargs):
        super().__init__(**kwargs)
        
        self.executor = executor
        self.output = PMAWOutput(output)
        self.main_thread = main_thread


    def _get(self, url, payload={}):
        try:
            self._impose_rate_limit()
            r = requests.get(url, params=payload)
            status = r.status_code
            reason = r.reason

            if status == 200:
                r = json.loads(r.text)

                # check if shards are down
                self.meta = Metadata(r.get("metadata", {}))
                total_results = self.meta.total_results

                if self.possible_results <= 0:
                    self.possible_results = total_results

                if total_results:
                    after, before = self.meta.ranges
                    if after and before:
                        self.resp_dict[(after, before)] = total_results

                if self.req.limit:
                    self.output.output_progress(self.req.limit, self.possible_results)
                else:
                    self.output.output_progress(self.possible_results, self.possible_results)

                return r["data"]
            else:
                if status != 429:
                    if reason:
                        log.warning(f"HTTP {status} - {reason}")
                        self.output.output_error(f"HTTP {status} - {reason}")
                    else:
                        log.warning(f"HTTP {status}")
                        self.output.output_error(f"HTTP {status}")
                if status == 404:
                    raise HTTPNotFoundError(f"HTTP {status} - {reason}")
                else:
                    # TODO: add custom error types for rate limit and other errors
                    raise HTTPError(f"HTTP {status} - {reason}")
        except:
            log.critical(CRITICAL_MESSAGE, exc_info=True)


    def _multithread(self, check_total=False):
        while len(self.req.req_list) > 0 and not self.output.cancel_is_set():

            # reset resp_dict which tracks remaining responses for timeslices
            self.resp_dict = {}

            # set number of futures created to batch size
            reqs = []
            if check_total:
                reqs.append(self.req.req_list.popleft())
            else:
                for i in range(min(len(self.req.req_list), self.batch_size)):
                    reqs.append(self.req.req_list.popleft())

            futures = {
                self.executor.submit(self._get, url_pay[0], url_pay[1]): url_pay
                for url_pay in reqs
            }

            self._futures_handler(futures, check_total)

            # reset attempts if no failures
            self._rate_limit._check_fail()

            # check if shards are down
            if self.meta.shards_are_down and (
                self.shards_down_behavior is not None
            ):
                shards_down_message = "Not all PushShift shards are active. Query results may be incomplete."
                log.warning(shards_down_message)

            if not check_total:
                self.num_batches += 1
                if self.num_batches % self.file_checkpoint == 0:
                    # cache current results
                    self.executor.submit(self.req.save_cache())
                self._print_stats("Checkpoint")
            else:
                break
        if not check_total:
            self._print_stats("Total")


    def _search(
        self,
        kind,
        max_ids_per_request=500,
        max_results_per_request=100,
        mem_safe=False,
        search_window=365,
        dataset="reddit",
        safe_exit=False,
        cache_dir=None,
        filter_fn=None,
        **kwargs,
    ):

        # TODO: remove this warning once 404s stop happening
        if kind == "submission_comment_ids":
            log.warning(
                "submission comment id search may return no results due to COLO switchover"
            )

        # raise error if aggs are requested
        if "aggs" in kwargs:
            err_msg = "Aggregations support for {} has not yet been implemented, please use the PSAW package for your request"
            raise NotImplementedError(err_msg.format(kwargs["aggs"]))

        self.meta = Metadata({})
        self.resp_dict = {}
        self.req = Request(
            copy.deepcopy(kwargs),
            filter_fn,
            kind,
            max_results_per_request,
            max_ids_per_request,
            mem_safe,
            safe_exit,
            cache_dir,
            self.praw,
        )

        # reset stat tracking
        self._reset()

        if kind == "submission_comment_ids":
            endpoint = f"{dataset}/submission/comment_ids/"
        else:
            endpoint = f"{dataset}/{kind}/search"

        url = self.base_url.format(endpoint=endpoint)

        self.possible_results = 0

        while (self.req.limit is None or self.req.limit > 0) and not self.output.cancel_is_set():
            # set/update limit
            if "ids" not in self.req.payload and len(self.req.req_list) == 0:
                # check to see how many results are remaining
                self.req.req_list.appendleft((url, self.req.payload))
                self._multithread(check_total=True)
                total_avail = self.meta.total_results

                if self.req.limit is None:
                    log.info(f"{total_avail} result(s) available in Pushshift")
                    self.req.limit = total_avail
                elif total_avail < self.req.limit:
                    log.info(
                        f"{self.req.limit - total_avail} result(s) not found in Pushshift"
                    )
                    log.info(f"{total_avail} total available")
                    self.req.limit = total_avail

            # generate payloads
            self.req.gen_url_payloads(url, self.batch_size, search_window)

            if self.req.limit > 0 and len(self.req.req_list) > 0:
                self._multithread()

        self.req.save_cache()
        return self.req.resp