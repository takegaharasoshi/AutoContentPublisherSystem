window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["luna-1b/U28"] = [
  {
    "case_id": "U28-e01",
    "record": {
      "comment_id": "U28-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "yes",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 167,
            "finish_reason": "stop",
            "latency_s": 7.376405,
            "model": "gpt-6-luna",
            "prompt_tokens": 3020,
            "reasoning_tokens": 92
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、以前にも「ウミガメのスープ」と呼ばれるものを飲んだとあります。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は以前にもウミガメのスープを飲んだことがありますか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 7.376431522978237,
      "luna_s": 7.376431522978237,
      "total_s": 24.00957553597982,
      "writer_s": 16.633144013001584
    }
  },
  {
    "case_id": "U28-e02",
    "record": {
      "comment_id": "U28-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "no",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 400,
            "finish_reason": "stop",
            "latency_s": 4.019661,
            "model": "gpt-6-luna",
            "prompt_tokens": 3023,
            "reasoning_tokens": 309
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "一つのはい／いいえ質問。味に覚えがあったのではなく、味の違いから過去の真相に気づいたためです。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。スープの味に覚えがあったからではないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男が泣いたのは、スープの味に覚えがあったからですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 4.019705537008122,
      "luna_s": 4.019705537008122,
      "total_s": 6.672399800008861,
      "writer_s": 2.6526942630007397
    }
  },
  {
    "case_id": "U28-e03",
    "record": {
      "comment_id": "U28-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "yes",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 162,
            "finish_reason": "stop",
            "latency_s": 7.359146,
            "model": "gpt-6-luna",
            "prompt_tokens": 3015,
            "reasoning_tokens": 93
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "男性は若いころ、船の事故で仲間と海を漂った経験があります。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！少しずつ聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は昔、遭難した経験があるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 7.3591955350129865,
      "luna_s": 7.3591955350129865,
      "total_s": 9.190641321009025,
      "writer_s": 1.8314457859960385
    }
  },
  {
    "case_id": "U28-e04",
    "record": {
      "comment_id": "U28-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "yes",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 741,
            "finish_reason": "stop",
            "latency_s": 6.581463,
            "model": "gpt-6-luna",
            "prompt_tokens": 3027,
            "reasoning_tokens": 659
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "昔の経験を思い出し、味の違いと確認を通じて真相に気づきます。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "本物だと聞いたことで、男の過去の記憶がよみがえったんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 6.5814923380094115,
      "luna_s": 6.5814923380094115,
      "total_s": 7.692117780010449,
      "writer_s": 1.1106254420010373
    }
  },
  {
    "case_id": "U28-e05",
    "record": {
      "comment_id": "U28-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "unknown",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "unknown",
          "bare_term": null,
          "debug": {
            "completion_tokens": 430,
            "finish_reason": "stop",
            "latency_s": 3.924459,
            "model": "gpt-6-luna",
            "prompt_tokens": 3023,
            "reasoning_tokens": 354
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "飲む前から疑っていたかは、問題文や確定事実から判断できません。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "それは答えに関わらないんだ。ほかのことも聞いてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "スープを飲む前から、男は本物かどうか疑っていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 3.9245078150124755,
      "luna_s": 3.9245078150124755,
      "total_s": 5.936528616031865,
      "writer_s": 2.012020801019389
    }
  },
  {
    "case_id": "U28-e06",
    "record": {
      "comment_id": "U28-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "irrelevant",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "completion_tokens": 233,
            "finish_reason": "stop",
            "latency_s": 2.743854,
            "model": "gpt-6-luna",
            "prompt_tokens": 3012,
            "reasoning_tokens": 162
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "店の場所は真相や確定事実に関係しないためです。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "そのレストランは海辺にありますか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.7438740269863047,
      "luna_s": 2.7438740269863047,
      "total_s": 6.8200554979848675,
      "writer_s": 4.076181470998563
    }
  },
  {
    "case_id": "U28-e07",
    "record": {
      "comment_id": "U28-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "irrelevant",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "completion_tokens": 374,
            "finish_reason": "stop",
            "latency_s": 8.669027,
            "model": "gpt-6-luna",
            "prompt_tokens": 3016,
            "reasoning_tokens": 294
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "シェフが男を知っていたかどうかは、真相の核心に関係しません。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "シェフは男のことを知っていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 8.669074826990254,
      "luna_s": 8.669074826990254,
      "total_s": 11.18433888501022,
      "writer_s": 2.515264058019966
    }
  },
  {
    "case_id": "U28-e08",
    "record": {
      "comment_id": "U28-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "yes",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 470,
            "finish_reason": "stop",
            "latency_s": 4.391868,
            "model": "gpt-6-luna",
            "prompt_tokens": 3024,
            "reasoning_tokens": 409
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "真相では、以前の出来事と飲んだものの正体に気づいています。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男はスープを飲んで、何か別のものを思い出したんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 4.391932273982093,
      "luna_s": 4.391932273982093,
      "total_s": 5.761736629996449,
      "writer_s": 1.369804356014356
    }
  },
  {
    "case_id": "U28-e09",
    "record": {
      "comment_id": "U28-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "irrelevant",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "completion_tokens": 244,
            "finish_reason": "stop",
            "latency_s": 38.626641,
            "model": "gpt-6-luna",
            "prompt_tokens": 3018,
            "reasoning_tokens": 166
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "誰がスープを運んだかは、男が泣いた理由に関係しません。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "スープを出したのは、その店のシェフ本人ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 38.626699473999906,
      "luna_s": 38.626699473999906,
      "total_s": 42.59698334700079,
      "writer_s": 3.9702838730008807
    }
  },
  {
    "case_id": "U28-e10",
    "record": {
      "comment_id": "U28-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "irrelevant",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "completion_tokens": 226,
            "finish_reason": "stop",
            "latency_s": 7.832744,
            "model": "gpt-6-luna",
            "prompt_tokens": 3020,
            "reasoning_tokens": 153
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "飼っていたかは、男が泣いた理由に関係しません。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。次のことも聞いてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は昔、ウミガメを飼っていたんでしょか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 7.832805076002842,
      "luna_s": 7.832805076002842,
      "total_s": 10.13719854800729,
      "writer_s": 2.304393472004449
    }
  },
  {
    "case_id": "U28-e11",
    "record": {
      "comment_id": "U28-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_multi"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 140,
            "finish_reason": "stop",
            "latency_s": 37.743959,
            "model": "gpt-6-luna",
            "prompt_tokens": 3031,
            "reasoning_tokens": 54
          },
          "error": null,
          "kind": "q_multi",
          "reason": "過去にウミガメを食べたか、出来事を思い出したかの二つを尋ねています。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。分けて聞いてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は過去にウミガメを食べたことがあるの？その時の出来事を思い出したの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 37.74400574999163,
      "luna_s": 37.74400574999163,
      "total_s": 45.95902467900305,
      "writer_s": 8.215018929011421
    }
  },
  {
    "case_id": "U28-e12",
    "record": {
      "comment_id": "U28-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_multi"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 253,
            "finish_reason": "stop",
            "latency_s": 2.601141,
            "model": "gpt-6-luna",
            "prompt_tokens": 3028,
            "reasoning_tokens": 173
          },
          "error": null,
          "kind": "q_multi",
          "reason": "味の違いと気づいた内容について、質問が二つあります。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。どちらから聞こうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "スープの味が記憶と違ったの？本物だと聞いて何かに気づいたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.6012020480120555,
      "luna_s": 2.6012020480120555,
      "total_s": 6.427937353000743,
      "writer_s": 3.826735304988688
    }
  },
  {
    "case_id": "U28-e13",
    "record": {
      "comment_id": "U28-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 208,
            "finish_reason": "stop",
            "latency_s": 2.086568,
            "model": "gpt-6-luna",
            "prompt_tokens": 3023,
            "reasoning_tokens": 122
          },
          "error": null,
          "kind": "q_open",
          "reason": "「なぜ」と理由を尋ねており、はい／いいえでは答えられないためです。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞き直してごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男はなぜ本物のウミガメかどうか確かめたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.086610244004987,
      "luna_s": 2.086610244004987,
      "total_s": 6.136151447019074,
      "writer_s": 4.049541203014087
    }
  },
  {
    "case_id": "U28-e14",
    "record": {
      "comment_id": "U28-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 205,
            "finish_reason": "stop",
            "latency_s": 2.164535,
            "model": "gpt-6-luna",
            "prompt_tokens": 3021,
            "reasoning_tokens": 123
          },
          "error": null,
          "kind": "q_open",
          "reason": "「何を思い出したか」を尋ねる、はい／いいえで答えられない質問です。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "何を思い出したのか、はい・いいえで答えられる形で聞いてみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "スープを飲んだとき、男は何を思い出したんでしょう？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.164603512996109,
      "luna_s": 2.164603512996109,
      "total_s": 7.861338317976333,
      "writer_s": 5.696734804980224
    }
  },
  {
    "case_id": "U28-e15",
    "record": {
      "comment_id": "U28-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 166,
            "finish_reason": "stop",
            "latency_s": 2.045089,
            "model": "gpt-6-luna",
            "prompt_tokens": 3023,
            "reasoning_tokens": 78
          },
          "error": null,
          "kind": "q_open",
          "reason": "過去に何があったかを尋ねる、はい・いいえで答えられない質問です。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる質問にして聞いてごらん。少しずつ絞っていこうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男が泣き崩れるまでに、どんな過去があったんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.0451543150120415,
      "luna_s": 2.0451543150120415,
      "total_s": 4.622050713020144,
      "writer_s": 2.5768963980081026
    }
  },
  {
    "case_id": "U28-e16",
    "record": {
      "comment_id": "U28-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_correct"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 241,
            "finish_reason": "stop",
            "latency_s": 2.673736,
            "model": "gpt-6-luna",
            "prompt_tokens": 3027,
            "reasoning_tokens": 129
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "昔飲んだスープが仲間の肉だったという核心を言い当てています。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "正解！昔飲んだスープは、亡くなった仲間の肉で作られていたんだ。仲間は彼を生かすため、ウミガメのスープだと伝えたんだよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "昔ウミガメのスープだと言われて飲んだものが、仲間の肉だったってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.673794523027027,
      "luna_s": 2.673794523027027,
      "total_s": 4.8428406070161145,
      "writer_s": 2.1690460839890875
    }
  },
  {
    "case_id": "U28-e17",
    "record": {
      "comment_id": "U28-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_correct"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 283,
            "finish_reason": "stop",
            "latency_s": 7.688206,
            "model": "gpt-6-luna",
            "prompt_tokens": 3046,
            "reasoning_tokens": 164
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "昔のスープが仲間の肉だったことと、味の違いで嘘に気づいた点を言い当てています。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "正解！昔飲んだのは仲間の肉で、仲間は男を生かすためウミガメのスープだと嘘をついたんだ。今日、本物の味でその嘘に気づいたんだね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "昔、仲間の肉をウミガメのスープだと言われて飲んだんだね。本物の味が違って、あの時の嘘に気づいたのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 7.688248603022657,
      "luna_s": 7.688248603022657,
      "total_s": 11.134138764027739,
      "writer_s": 3.4458901610050816
    }
  },
  {
    "case_id": "U28-e18",
    "record": {
      "comment_id": "U28-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_close"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 177,
            "finish_reason": "stop",
            "latency_s": 7.488505,
            "model": "gpt-6-luna",
            "prompt_tokens": 3033,
            "reasoning_tokens": 104
          },
          "error": null,
          "kind": "guess_close",
          "reason": "昔、仲間からウミガメのスープと言われて飲んだ点には触れていますが、核心の材料には触れていません。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "漂流していたとき、仲間からウミガメのスープだと言われて飲んだことがあったんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 7.488556272990536,
      "luna_s": 7.488556272990536,
      "total_s": 9.00484666597913,
      "writer_s": 1.5162903929885942
    }
  },
  {
    "case_id": "U28-e19",
    "record": {
      "comment_id": "U28-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_correct"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 832,
            "finish_reason": "stop",
            "latency_s": 6.393726,
            "model": "gpt-6-luna",
            "prompt_tokens": 3047,
            "reasoning_tokens": 723
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "コアの要点を言い当てており、仲間全員が助かったかを尋ねています。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "正解！仲間の何人かは亡くなり、その肉をウミガメのスープだと言って男に飲ませたんだ。男は生き延びて帰り、今日、本物との味の違いから真相を知ったんだよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "仲間の肉をウミガメのスープだと言われて飲んだんだね。でもそのとき仲間はみんな助かって、あとで一緒に帰れたのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 6.393756258010399,
      "luna_s": 6.393756258010399,
      "total_s": 27.601247761020204,
      "writer_s": 21.207491503009805
    }
  },
  {
    "case_id": "U28-e20",
    "record": {
      "comment_id": "U28-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_wrong"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 149,
            "finish_reason": "stop",
            "latency_s": 7.363304,
            "model": "gpt-6-luna",
            "prompt_tokens": 3030,
            "reasoning_tokens": 86
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "涙の理由を推測していますが、コアの仕掛けには触れていません。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。ほかの理由も考えてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男はウミガメが大好きで、食べてしまったことが悲しくて泣いたんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 7.363354046014138,
      "luna_s": 7.363354046014138,
      "total_s": 8.954347320017405,
      "writer_s": 1.5909932740032673
    }
  },
  {
    "case_id": "U28-e21",
    "record": {
      "comment_id": "U28-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_wrong"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 198,
            "finish_reason": "stop",
            "latency_s": 2.516862,
            "model": "gpt-6-luna",
            "prompt_tokens": 3035,
            "reasoning_tokens": 128
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "今日のスープに昔飼っていたカメが使われたという推理で、核心には触れていません。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。別の理由を考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "子どものころに飼っていたカメがこのスープに使われたと思い込んで、悲しくなったんだと思う。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.5169150459987577,
      "luna_s": 2.5169150459987577,
      "total_s": 6.629754737979965,
      "writer_s": 4.112839691981208
    }
  },
  {
    "case_id": "U28-t01",
    "record": {
      "comment_id": "U28-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": "仲間の肉",
          "debug": {
            "completion_tokens": 212,
            "finish_reason": "stop",
            "latency_s": 2.33594,
            "model": "gpt-6-luna",
            "prompt_tokens": 3006,
            "reasoning_tokens": 126
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句だけのコメントなので、推理ではなくq_openです。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "仲間の肉が何のことか、もう少し詳しく教えて！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "仲間の肉？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.3359881760261487,
      "luna_s": 2.3359881760261487,
      "total_s": 6.930570649041329,
      "writer_s": 4.59458247301518
    }
  },
  {
    "case_id": "U28-t02",
    "record": {
      "comment_id": "U28-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": "レモン",
          "debug": {
            "completion_tokens": 196,
            "finish_reason": "stop",
            "latency_s": 2.312295,
            "model": "gpt-6-luna",
            "prompt_tokens": 3004,
            "reasoning_tokens": 118
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句だけのコメントなので、q_openと判定しました。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "レモンの何が気になるのかな？はい・いいえで答えられる質問にして聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "レモン",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.312341333978111,
      "luna_s": 2.312341333978111,
      "total_s": 11.802713937999215,
      "writer_s": 9.490372604021104
    }
  },
  {
    "case_id": "c-ask_howto-04",
    "record": {
      "comment_id": "c-ask_howto-04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "ask_howto"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 175,
            "finish_reason": "stop",
            "latency_s": 17.494105,
            "model": "gpt-6-luna",
            "prompt_tokens": 3011,
            "reasoning_tokens": 99
          },
          "error": null,
          "kind": "ask_howto",
          "reason": "質問への返答があるか、遊び方について尋ねています。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "うん！はい・いいえで答えられる質問をコメントしてね。私が答えるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "質問したら返事もらえるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 17.49413262499729,
      "luna_s": 17.49413262499729,
      "total_s": 19.424753060011426,
      "writer_s": 1.9306204350141343
    }
  },
  {
    "case_id": "c-cheer-03",
    "record": {
      "comment_id": "c-cheer-03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "cheer"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 185,
            "finish_reason": "stop",
            "latency_s": 2.345113,
            "model": "gpt-6-luna",
            "prompt_tokens": 3009,
            "reasoning_tokens": 130
          },
          "error": null,
          "kind": "cheer",
          "reason": "更新を楽しみにしているという応援のコメントです。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ありがとう！楽しみにしててね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "更新たのしみにしてる〜",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.3451546340074856,
      "luna_s": 2.3451546340074856,
      "total_s": 6.12893786400673,
      "writer_s": 3.783783229999244
    }
  },
  {
    "case_id": "c-complaint-02",
    "record": {
      "comment_id": "c-complaint-02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "complaint"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 264,
            "finish_reason": "stop",
            "latency_s": 2.92109,
            "model": "gpt-6-luna",
            "prompt_tokens": 3013,
            "reasoning_tokens": 200
          },
          "error": null,
          "kind": "complaint",
          "reason": "前の投稿との設定の重複を指摘する、問題への意見です。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "教えてくれてありがとう。確認するね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "前の投稿と設定が被ってる気がする",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.9211436140176374,
      "luna_s": 2.9211436140176374,
      "total_s": 4.4711004810233135,
      "writer_s": 1.549956867005676
    }
  },
  {
    "case_id": "c-troll-01",
    "record": {
      "comment_id": "c-troll-01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "troll"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 77,
            "finish_reason": "stop",
            "latency_s": 1.572456,
            "model": "gpt-6-luna",
            "prompt_tokens": 3011,
            "reasoning_tokens": 22
          },
          "error": null,
          "kind": "troll",
          "reason": "意味の取れない文字の連続で、問題への推理や質問ではありません。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "質問なら、はい・いいえで答えるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "ぬぬぬぬぬ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 1.572506517986767,
      "luna_s": 1.572506517986767,
      "total_s": 1.572556397994049,
      "writer_s": 4.988000728189945e-05
    }
  },
  {
    "case_id": "c-spam-05",
    "record": {
      "comment_id": "c-spam-05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "spam"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 118,
            "finish_reason": "stop",
            "latency_s": 1.76492,
            "model": "gpt-6-luna",
            "prompt_tokens": 3016,
            "reasoning_tokens": 66
          },
          "error": null,
          "kind": "spam",
          "reason": "プレゼント応募への誘導と外部リンクを含む宣伝コメントです。"
        }
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "no_reply",
        "text": null
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "無料プレゼント応募は固定リンクから→ https://example.invalid/gift",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 1.7649697070010006,
      "luna_s": 1.7649697070010006,
      "total_s": 1.7649739730113652,
      "writer_s": 4.2660103645175695e-06
    }
  }
];
