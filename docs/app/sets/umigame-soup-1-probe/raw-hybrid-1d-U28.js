window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["hybrid-1d/U28"] = [
  {
    "case_id": "U28-e01",
    "record": {
      "comment_id": "U28-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4379,
            "latency_s": 1.299428,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 256,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.17,
                "question": 0.83
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.68,
                "point_1": 0.02
              },
              "C": 0.58,
              "D": {
                "irrelevant": 0.0,
                "no": 0.0,
                "yes": 1.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
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
        "text": "はい！ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は以前にもウミガメのスープを飲んだことがありますか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2997973519959487,
      "judge_s": 7.376431522978237,
      "luna_s": 7.376431522978237,
      "total_s": 8.676992458000313,
      "writer_s": 1.3005609350220766
    }
  },
  {
    "case_id": "U28-e02",
    "record": {
      "comment_id": "U28-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "guess_demoted": true,
            "input_tokens": 4379,
            "latency_s": 1.251515,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 256,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.97,
                "question": 0.03
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.02,
                "q_yesno": 0.98
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.05,
                "point_1": 0.02
              },
              "C": 0.76,
              "D": {
                "irrelevant": 0.0,
                "no": 0.93,
                "yes": 0.07
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
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
      "shadow_mismatch": false,
      "text": "男が泣いたのは、スープの味に覚えがあったからですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2518042970041279,
      "judge_s": 4.019705537008122,
      "luna_s": 4.019705537008122,
      "total_s": 5.239871862024302,
      "writer_s": 1.22016632501618
    }
  },
  {
    "case_id": "U28-e03",
    "record": {
      "comment_id": "U28-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4325,
            "latency_s": 1.230527,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 256,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.84,
                "question": 0.16
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02,
                "point_1": 0.01
              },
              "C": 0.62,
              "D": {
                "irrelevant": 0.0,
                "no": 0.0,
                "yes": 1.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
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
        "text": "はい！ほかにも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は昔、遭難した経験があるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.230848662002245,
      "judge_s": 7.3591955350129865,
      "luna_s": 7.3591955350129865,
      "total_s": 11.171297916996991,
      "writer_s": 3.8121023819840048
    }
  },
  {
    "case_id": "U28-e04",
    "record": {
      "comment_id": "U28-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "guess_demoted": true,
            "input_tokens": 4403,
            "latency_s": 1.219217,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 256,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.96,
                "question": 0.04
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.02,
                "q_yesno": 0.98
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.04,
                "point_1": 0.03
              },
              "C": 0.71,
              "D": {
                "irrelevant": 0.0,
                "no": 0.09,
                "yes": 0.91
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.03"
        },
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
      "shadow_mismatch": false,
      "text": "本物だと聞いたことで、男の過去の記憶がよみがえったんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.219428684009472,
      "judge_s": 6.5814923380094115,
      "luna_s": 6.5814923380094115,
      "total_s": 10.176437248999719,
      "writer_s": 3.594944910990307
    }
  },
  {
    "case_id": "U28-e05",
    "record": {
      "comment_id": "U28-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": "unknown",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4385,
            "latency_s": 1.188149,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 256,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.11,
                "question": 0.89
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.05,
                "point_1": 0.05
              },
              "C": 0.54,
              "D": {
                "irrelevant": 0.14,
                "no": 0.53,
                "yes": 0.33
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.05"
        },
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
      "shadow_mismatch": false,
      "text": "スープを飲む前から、男は本物かどうか疑っていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1883304610091727,
      "judge_s": 3.9245078150124755,
      "luna_s": 3.9245078150124755,
      "total_s": 6.010062751010992,
      "writer_s": 2.085554935998516
    }
  },
  {
    "case_id": "U28-e06",
    "record": {
      "comment_id": "U28-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4319,
            "latency_s": 1.446831,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 258,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.11,
                "question": 0.89
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.01,
                "point_1": 0.01
              },
              "C": 0.22,
              "D": {
                "irrelevant": 0.99,
                "no": 0.01,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
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
        "text": "関係ないよ。次はどう聞こうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "そのレストランは海辺にありますか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.4470989359833766,
      "judge_s": 2.7438740269863047,
      "luna_s": 2.7438740269863047,
      "total_s": 3.982444036984816,
      "writer_s": 1.2385700099985115
    }
  },
  {
    "case_id": "U28-e07",
    "record": {
      "comment_id": "U28-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4331,
            "latency_s": 1.165868,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 256,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.13,
                "question": 0.87
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02,
                "point_1": 0.03
              },
              "C": 0.58,
              "D": {
                "irrelevant": 0.14,
                "no": 0.86,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
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
      "shadow_mismatch": true,
      "text": "シェフは男のことを知っていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.166223266016459,
      "judge_s": 8.669074826990254,
      "luna_s": 8.669074826990254,
      "total_s": 9.848993002990028,
      "writer_s": 1.1799181759997737
    }
  },
  {
    "case_id": "U28-e08",
    "record": {
      "comment_id": "U28-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4379,
            "latency_s": 1.19839,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 256,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.9,
                "question": 0.1
              },
              "A2": {
                "q_multi": 0.04,
                "q_open": 0.03,
                "q_yesno": 0.93
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.05,
                "point_1": 0.02
              },
              "C": 0.61,
              "D": {
                "irrelevant": 0.0,
                "no": 0.03,
                "yes": 0.97
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
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
        "text": "はい！その調子で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男はスープを飲んで、何か別のものを思い出したんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1986903429788072,
      "judge_s": 4.391932273982093,
      "luna_s": 4.391932273982093,
      "total_s": 5.835331299982499,
      "writer_s": 1.4433990260004066
    }
  },
  {
    "case_id": "U28-e09",
    "record": {
      "comment_id": "U28-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4355,
            "latency_s": 1.326889,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 256,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.01,
                "question": 0.99
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02,
                "point_1": 0.01
              },
              "C": 0.37,
              "D": {
                "irrelevant": 0.24,
                "no": 0.04,
                "yes": 0.72
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
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
        "text": "関係ないよ。ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "スープを出したのは、その店のシェフ本人ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.3272099930036347,
      "judge_s": 38.626699473999906,
      "luna_s": 38.626699473999906,
      "total_s": 40.14272803001222,
      "writer_s": 1.5160285560123157
    }
  },
  {
    "case_id": "U28-e10",
    "record": {
      "comment_id": "U28-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "guess_demoted": true,
            "input_tokens": 4343,
            "latency_s": 1.307394,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 256,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.96,
                "question": 0.04
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.03,
                "point_1": 0.02
              },
              "C": 0.69,
              "D": {
                "irrelevant": 0.43,
                "no": 0.57,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
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
        "text": "関係ないよ。ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "男は昔、ウミガメを飼っていたんでしょか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.3077298610005528,
      "judge_s": 7.832805076002842,
      "luna_s": 7.832805076002842,
      "total_s": 9.489105955988634,
      "writer_s": 1.6563008799857926
    }
  },
  {
    "case_id": "U28-e11",
    "record": {
      "comment_id": "U28-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "input_tokens": 2167,
            "latency_s": 0.579715,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 154,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.91,
                "question": 0.09
              },
              "A2": {
                "q_multi": 0.95,
                "q_open": 0.0,
                "q_yesno": 0.05
              },
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_multi",
          "reason": "段A=question→q_multi"
        },
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
        "text": "質問はひとつずつコメントしてね。どちらか一つから聞いてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は過去にウミガメを食べたことがあるの？その時の出来事を思い出したの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.5798578989924863,
      "judge_s": 37.74400574999163,
      "luna_s": 37.74400574999163,
      "total_s": 45.935968361998675,
      "writer_s": 8.191962612007046
    }
  },
  {
    "case_id": "U28-e12",
    "record": {
      "comment_id": "U28-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "input_tokens": 2155,
            "latency_s": 0.653304,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 154,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.94,
                "question": 0.06
              },
              "A2": {
                "q_multi": 0.95,
                "q_open": 0.01,
                "q_yesno": 0.04
              },
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_multi",
          "reason": "段A=question→q_multi"
        },
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
        "text": "質問はひとつずつ聞いてごらん☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "スープの味が記憶と違ったの？本物だと聞いて何かに気づいたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.6534870059986133,
      "judge_s": 2.6012020480120555,
      "luna_s": 2.6012020480120555,
      "total_s": 4.224818779010093,
      "writer_s": 1.6236167309980374
    }
  },
  {
    "case_id": "U28-e13",
    "record": {
      "comment_id": "U28-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 2660,
            "latency_s": 0.959973,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 176,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.01,
                "question": 0.99
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.98,
                "q_yesno": 0.02
              },
              "A3": 0.11,
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.11"
        },
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
        "text": "男が確かめた理由について、はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男はなぜ本物のウミガメかどうか確かめたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.9602092309796717,
      "judge_s": 2.086610244004987,
      "luna_s": 2.086610244004987,
      "total_s": 4.634423173003597,
      "writer_s": 2.54781292899861
    }
  },
  {
    "case_id": "U28-e14",
    "record": {
      "comment_id": "U28-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 2664,
            "latency_s": 0.76194,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 176,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.66,
                "question": 0.34
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 1.0,
                "q_yesno": 0.0
              },
              "A3": 0.06,
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.06"
        },
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
        "text": "男が何を思い出したのか、はい・いいえで答えられる形で聞いてみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "スープを飲んだとき、男は何を思い出したんでしょう？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.7621611320064403,
      "judge_s": 2.164603512996109,
      "luna_s": 2.164603512996109,
      "total_s": 4.148957169993082,
      "writer_s": 1.9843536569969729
    }
  },
  {
    "case_id": "U28-e15",
    "record": {
      "comment_id": "U28-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 2672,
            "latency_s": 0.825044,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 176,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.08,
                "question": 0.92
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 1.0,
                "q_yesno": 0.0
              },
              "A3": 0.04,
              "A_bare": 0.03
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.04"
        },
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
        "text": "男の過去について、はい・いいえで答えられる形にして聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男が泣き崩れるまでに、どんな過去があったんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.8252764460048638,
      "judge_s": 2.0451543150120415,
      "luna_s": 2.0451543150120415,
      "total_s": 6.058623570017517,
      "writer_s": 4.013469255005475
    }
  },
  {
    "case_id": "U28-e16",
    "record": {
      "comment_id": "U28-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "consensus_ok",
        "kind": "guess_correct"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "input_tokens": 2098,
            "latency_s": 0.620402,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 150,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.98,
                "question": 0.02
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.92,
                "point_1": 0.85
              }
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.85"
        },
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
        "source": "template",
        "text": "正解！男は遭難中、ウミガメのスープだと言われて亡くなった仲間の肉を飲んでいた。本物の味でそれに気づいた。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "昔ウミガメのスープだと言われて飲んだものが、仲間の肉だったってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.620733249001205,
      "judge_s": 2.673794523027027,
      "luna_s": 2.673794523027027,
      "total_s": 2.673808662017109,
      "writer_s": 1.4138990081846714e-05
    }
  },
  {
    "case_id": "U28-e17",
    "record": {
      "comment_id": "U28-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "consensus_ok",
        "kind": "guess_correct"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "input_tokens": 2149,
            "latency_s": 0.654004,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 150,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 1.0,
                "question": 0.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.96,
                "point_1": 0.89
              }
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.89"
        },
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
        "source": "template",
        "text": "正解！男は遭難中、ウミガメのスープだと言われて亡くなった仲間の肉を飲んでいた。本物の味でそれに気づいた。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "昔、仲間の肉をウミガメのスープだと言われて飲んだんだね。本物の味が違って、あの時の嘘に気づいたのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.654244816978462,
      "judge_s": 7.688248603022657,
      "luna_s": 7.688248603022657,
      "total_s": 7.6882529870199505,
      "writer_s": 4.383997293189168e-06
    }
  },
  {
    "case_id": "U28-e18",
    "record": {
      "comment_id": "U28-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "input_tokens": 2116,
            "latency_s": 0.645673,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 150,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.01,
                "request": 0.0
              },
              "A1b": {
                "guess": 1.0,
                "question": 0.0
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.94,
                "point_1": 0.07
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.07"
        },
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
        "text": "惜しい！質問しながら推理を続けてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "漂流していたとき、仲間からウミガメのスープだと言われて飲んだことがあったんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.6458849289920181,
      "judge_s": 7.488556272990536,
      "luna_s": 7.488556272990536,
      "total_s": 9.1941258769657,
      "writer_s": 1.7055696039751638
    }
  },
  {
    "case_id": "U28-e19",
    "record": {
      "comment_id": "U28-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "consensus_ok",
        "kind": "guess_correct"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 2728,
            "latency_s": 0.843294,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 196,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.92,
                "question": 0.08
              },
              "A2": {
                "q_multi": 0.38,
                "q_open": 0.01,
                "q_yesno": 0.61
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.93,
                "point_1": 0.83
              }
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=question→guess_correct, 要点最低=0.83"
        },
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
        "source": "template",
        "text": "正解！男は遭難中、ウミガメのスープだと言われて亡くなった仲間の肉を飲んでいた。本物の味でそれに気づいた。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "仲間の肉をウミガメのスープだと言われて飲んだんだね。でもそのとき仲間はみんな助かって、あとで一緒に帰れたのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.843544125003973,
      "judge_s": 6.393756258010399,
      "luna_s": 6.393756258010399,
      "total_s": 6.393764338019537,
      "writer_s": 8.080009138211608e-06
    }
  },
  {
    "case_id": "U28-e20",
    "record": {
      "comment_id": "U28-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "guess_demoted": true,
            "input_tokens": 4427,
            "latency_s": 1.314805,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 256,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 1.0,
                "question": 0.0
              },
              "A2": {
                "q_multi": 0.03,
                "q_open": 0.13,
                "q_yesno": 0.84
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.14,
                "point_1": 0.08
              },
              "C": 0.48,
              "D": {
                "irrelevant": 0.0,
                "no": 1.0,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.08"
        },
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
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "男はウミガメが大好きで、食べてしまったことが悲しくて泣いたんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.3151650250074454,
      "judge_s": 7.363354046014138,
      "luna_s": 7.363354046014138,
      "total_s": 8.548687559028622,
      "writer_s": 1.1853335130144842
    }
  },
  {
    "case_id": "U28-e21",
    "record": {
      "comment_id": "U28-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "input_tokens": 2131,
            "latency_s": 0.615945,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 150,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.01,
                "request": 0.0
              },
              "A1b": {
                "guess": 1.0,
                "question": 0.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.25,
                "point_1": 0.21
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.21"
        },
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
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "子どものころに飼っていたカメがこのスープに使われたと思い込んで、悲しくなったんだと思う。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.6162741050065961,
      "judge_s": 2.5169150459987577,
      "luna_s": 2.5169150459987577,
      "total_s": 3.451066481997259,
      "writer_s": 0.9341514359985013
    }
  },
  {
    "case_id": "U28-t01",
    "record": {
      "comment_id": "U28-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": null,
          "bare_term": "仲間の肉",
          "debug": {
            "calls": 1,
            "input_tokens": 929,
            "latency_s": 0.173525,
            "model": "jev-latest",
            "output_tokens": 78,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A_bare": 0.84
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.84"
        },
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
      "shadow_mismatch": false,
      "text": "仲間の肉？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.17362348598544486,
      "judge_s": 2.3359881760261487,
      "luna_s": 2.3359881760261487,
      "total_s": 4.979247617040528,
      "writer_s": 2.6432594410143793
    }
  },
  {
    "case_id": "U28-t02",
    "record": {
      "comment_id": "U28-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": null,
          "bare_term": "レモン",
          "debug": {
            "calls": 1,
            "input_tokens": 927,
            "latency_s": 0.21989,
            "model": "jev-latest",
            "output_tokens": 78,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A_bare": 0.97
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.97"
        },
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
        "source": "fallback_template",
        "text": "レモンがどうしたのか聞かせてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "レモン",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.2199422730191145,
      "judge_s": 2.312341333978111,
      "luna_s": 2.312341333978111,
      "total_s": 7.627443052973831,
      "writer_s": 5.31510171899572
    }
  },
  {
    "case_id": "c-ask_howto-04",
    "record": {
      "comment_id": "c-ask_howto-04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1431,
            "latency_s": 0.332886,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 124,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.03,
                "reaction": 0.0,
                "request": 0.97
              },
              "A2": {
                "ask_hint": 0.0,
                "ask_howto": 1.0,
                "ask_spoiler": 0.0
              },
              "A_bare": 0.03
            }
          },
          "error": null,
          "kind": "ask_howto",
          "reason": "段A=request→ask_howto"
        },
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
        "text": "はい、はい・いいえで答えられる質問をコメントすると、探偵が答えるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "質問したら返事もらえるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.33295693699619733,
      "judge_s": 17.49413262499729,
      "luna_s": 17.49413262499729,
      "total_s": 18.553200583002763,
      "writer_s": 1.0590679580054712
    }
  },
  {
    "case_id": "c-cheer-03",
    "record": {
      "comment_id": "c-cheer-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1588,
            "latency_s": 0.387458,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 149,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 1.0,
                "request": 0.0
              },
              "A2": {
                "chat": 0.02,
                "cheer": 0.9,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.04,
                "mention": 0.0,
                "request": 0.04
              },
              "A_bare": 0.07
            }
          },
          "error": null,
          "kind": "cheer",
          "reason": "段A=reaction→cheer"
        },
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
        "text": "ありがとう！更新も楽しみにしててね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "更新たのしみにしてる〜",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.38775741000426933,
      "judge_s": 2.3451546340074856,
      "luna_s": 2.3451546340074856,
      "total_s": 5.624238301010337,
      "writer_s": 3.279083667002851
    }
  },
  {
    "case_id": "c-complaint-02",
    "record": {
      "comment_id": "c-complaint-02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1598,
            "latency_s": 0.386183,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 149,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.03,
                "reaction": 0.97,
                "request": 0.0
              },
              "A2": {
                "chat": 0.02,
                "cheer": 0.0,
                "complaint": 0.58,
                "greeting": 0.0,
                "impression": 0.4,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.07
            }
          },
          "error": null,
          "kind": "complaint",
          "reason": "段A=reaction→complaint"
        },
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
        "text": "教えてくれてありがとう、確認するね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "前の投稿と設定が被ってる気がする",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.38636093999957666,
      "judge_s": 2.9211436140176374,
      "luna_s": 2.9211436140176374,
      "total_s": 4.093298843014054,
      "writer_s": 1.1721552289964166
    }
  },
  {
    "case_id": "c-troll-01",
    "record": {
      "comment_id": "c-troll-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1472,
            "latency_s": 0.374372,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
            "probabilities": {
              "A1": {
                "inappropriate": 0.83,
                "other": 0.0,
                "question_or_guess": 0.02,
                "reaction": 0.15,
                "request": 0.0
              },
              "A2": {
                "abuse": 0.0,
                "personal_info": 0.0,
                "spam": 0.0,
                "troll": 1.0
              },
              "A_bare": 0.42
            }
          },
          "error": null,
          "kind": "troll",
          "reason": "段A=inappropriate→troll"
        },
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
      "shadow_mismatch": false,
      "text": "ぬぬぬぬぬ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.374498766992474,
      "judge_s": 1.572506517986767,
      "luna_s": 1.572506517986767,
      "total_s": 1.5725206779607106,
      "writer_s": 1.4159973943606019e-05
    }
  },
  {
    "case_id": "c-spam-05",
    "record": {
      "comment_id": "c-spam-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
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
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 0,
            "input_tokens": 0,
            "latency_s": 0.0,
            "model": "jev-latest",
            "output_tokens": 0,
            "probabilities": {}
          },
          "error": null,
          "kind": "spam",
          "reason": "段0規則: spam"
        },
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
      "shadow_mismatch": false,
      "text": "無料プレゼント応募は固定リンクから→ https://example.invalid/gift",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 3.078399458900094e-05,
      "judge_s": 1.7649697070010006,
      "luna_s": 1.7649697070010006,
      "total_s": 1.7649727140087634,
      "writer_s": 3.0070077627897263e-06
    }
  }
];
