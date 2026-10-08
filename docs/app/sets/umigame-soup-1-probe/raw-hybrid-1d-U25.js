window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["hybrid-1d/U25"] = [
  {
    "case_id": "U25-e01",
    "record": {
      "comment_id": "U25-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 4571,
            "latency_s": 1.300911,
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
                "guess": 0.87,
                "question": 0.13
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.03,
                  "hit": 0.01
                }
              },
              "C": 0.46,
              "D": {
                "irrelevant": 0.0,
                "no": 1.0,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 233,
            "finish_reason": "stop",
            "latency_s": 3.270122,
            "model": "gpt-6-luna",
            "prompt_tokens": 3261,
            "reasoning_tokens": 163
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、二人は何も賭けていないとされています。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 75,
          "latency_s": 1.68598,
          "model": "gpt-6-luna",
          "prompt_tokens": 1431,
          "reasoning_tokens": 45,
          "slot": "判定語 + 一言"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "中学時代に二人で何か賭けをしてたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.3011095359688625,
      "judge_s": 3.270175585988909,
      "luna_s": 3.270175585988909,
      "total_s": 4.95713352097664,
      "writer_s": 1.6869579349877313
    }
  },
  {
    "case_id": "U25-e02",
    "record": {
      "comment_id": "U25-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 4607,
            "latency_s": 1.259668,
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
                "guess": 0.35,
                "question": 0.65
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.02,
                  "hit": 0.01
                }
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
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 393,
            "finish_reason": "stop",
            "latency_s": 4.37707,
            "model": "gpt-6-luna",
            "prompt_tokens": 3260,
            "reasoning_tokens": 314
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "「勝った」が長く続いた勝負の結果を指すかという一問で、真相と一致します。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 36,
          "latency_s": 1.509462,
          "model": "gpt-6-luna",
          "prompt_tokens": 1428,
          "reasoning_tokens": 17,
          "slot": "判定語だけ"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "「勝った」は、昔した勝負の結果について言ってるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.2600104919401929,
      "judge_s": 4.3771204489748925,
      "luna_s": 4.3771204489748925,
      "total_s": 5.898438400006853,
      "writer_s": 1.5213179510319605
    }
  },
  {
    "case_id": "U25-e03",
    "record": {
      "comment_id": "U25-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 4583,
            "latency_s": 1.26592,
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
                "guess": 0.37,
                "question": 0.63
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.04,
                  "hit": 0.02
                }
              },
              "C": 0.41,
              "D": {
                "irrelevant": 0.0,
                "no": 0.01,
                "yes": 0.99
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
            "completion_tokens": 237,
            "finish_reason": "stop",
            "latency_s": 3.035514,
            "model": "gpt-6-luna",
            "prompt_tokens": 3261,
            "reasoning_tokens": 173
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "真相では、二人は毎年年賀状を送り合っていました。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 29,
          "latency_s": 1.643979,
          "model": "gpt-6-luna",
          "prompt_tokens": 1429,
          "reasoning_tokens": 10,
          "slot": "判定語だけ"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "友人は毎年ずっと年賀状を送り続けていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.2662770509487018,
      "judge_s": 3.0355653499718755,
      "luna_s": 3.0355653499718755,
      "total_s": 4.680577069986612,
      "writer_s": 1.645011720014736
    }
  },
  {
    "case_id": "U25-e04",
    "record": {
      "comment_id": "U25-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 4517,
            "latency_s": 1.250607,
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
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.03,
              "B": {
                "point_0": {
                  "close": 0.01,
                  "hit": 0.01
                }
              },
              "C": 0.6,
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
            "completion_tokens": 197,
            "finish_reason": "stop",
            "latency_s": 3.207946,
            "model": "gpt-6-luna",
            "prompt_tokens": 3253,
            "reasoning_tokens": 132
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、二人は中学の同級生とあります。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 13,
          "latency_s": 1.868008,
          "model": "gpt-6-luna",
          "prompt_tokens": 1421,
          "reasoning_tokens": 0,
          "slot": "判定語だけ"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "二人は中学の同級生ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.2508741019992158,
      "judge_s": 3.208017229917459,
      "luna_s": 3.208017229917459,
      "total_s": 5.076963044935837,
      "writer_s": 1.8689458150183782
    }
  },
  {
    "case_id": "U25-e05",
    "record": {
      "comment_id": "U25-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 4565,
            "latency_s": 1.276263,
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
                "guess": 0.74,
                "question": 0.26
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.03,
              "B": {
                "point_0": {
                  "close": 0.39999999999999997,
                  "hit": 0.04
                }
              },
              "C": 0.7,
              "D": {
                "irrelevant": 0.0,
                "no": 0.02,
                "yes": 0.98
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.04"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 377,
            "finish_reason": "stop",
            "latency_s": 4.329658,
            "model": "gpt-6-luna",
            "prompt_tokens": 3259,
            "reasoning_tokens": 304
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "最後の年賀状には、勝負の決着を示す言葉が書かれていました。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 27,
          "latency_s": 2.118355,
          "model": "gpt-6-luna",
          "prompt_tokens": 1427,
          "reasoning_tokens": 8,
          "slot": "判定語だけ"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "年賀状に勝負の答えが書かれていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.2765801859786734,
      "judge_s": 4.32972816308029,
      "luna_s": 4.32972816308029,
      "total_s": 6.449150709086098,
      "writer_s": 2.119422546005808
    }
  },
  {
    "case_id": "U25-e06",
    "record": {
      "comment_id": "U25-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 4583,
            "latency_s": 1.175816,
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
                "guess": 0.66,
                "question": 0.34
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.01,
                  "hit": 0.01
                }
              },
              "C": 0.56,
              "D": {
                "irrelevant": 0.44,
                "no": 0.53,
                "yes": 0.03
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
            "completion_tokens": 362,
            "finish_reason": "stop",
            "latency_s": 4.237679,
            "model": "gpt-6-luna",
            "prompt_tokens": 3260,
            "reasoning_tokens": 275
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "友人が元気に暮らしている事実はありますが、男が心配していたかは示されていません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 106,
          "latency_s": 1.584067,
          "model": "gpt-6-luna",
          "prompt_tokens": 1431,
          "reasoning_tokens": 73,
          "slot": "判定語 + 復唱"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は友人がまだ生きているか気にしていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.1762437319848686,
      "judge_s": 4.237704842933454,
      "luna_s": 4.237704842933454,
      "total_s": 5.822344474843703,
      "writer_s": 1.5846396319102496
    }
  },
  {
    "case_id": "U25-e07",
    "record": {
      "comment_id": "U25-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 4565,
            "latency_s": 1.231064,
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
                "guess": 0.31,
                "question": 0.69
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.0,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.01,
                  "hit": 0.01
                }
              },
              "C": 0.37,
              "D": {
                "irrelevant": 0.36,
                "no": 0.42,
                "yes": 0.22
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
            "completion_tokens": 399,
            "finish_reason": "stop",
            "latency_s": 4.395914,
            "model": "gpt-6-luna",
            "prompt_tokens": 3258,
            "reasoning_tokens": 315
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "男が元日に受け取ったことは分かりますが、もう一人の受取日は定まっていません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 95,
          "latency_s": 1.488024,
          "model": "gpt-6-luna",
          "prompt_tokens": 1429,
          "reasoning_tokens": 62,
          "slot": "判定語 + 復唱"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "二人とも元日に年賀状を受け取ったんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.2313730319729075,
      "judge_s": 4.395943189971149,
      "luna_s": 4.395943189971149,
      "total_s": 5.884371787891723,
      "writer_s": 1.4884285979205742
    }
  },
  {
    "case_id": "U25-e08",
    "record": {
      "comment_id": "U25-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 4541,
            "latency_s": 1.201989,
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
                "guess": 0.03,
                "question": 0.97
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.26,
              "D": {
                "irrelevant": 0.08,
                "no": 0.0,
                "yes": 0.92
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 278,
            "finish_reason": "stop",
            "latency_s": 4.033432,
            "model": "gpt-6-luna",
            "prompt_tokens": 3256,
            "reasoning_tokens": 205
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "中学の同級生なので、年齢も同じくらいと考えられます。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 90,
          "latency_s": 2.851338,
          "model": "gpt-6-luna",
          "prompt_tokens": 1427,
          "reasoning_tokens": 56,
          "slot": "判定語 + 復唱"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！友人は男と同じくらいの年齢だよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "友人は男と同じくらいの年齢ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.202254706993699,
      "judge_s": 4.033487722976133,
      "luna_s": 4.033487722976133,
      "total_s": 6.885729526984505,
      "writer_s": 2.852241804008372
    }
  },
  {
    "case_id": "U25-e09",
    "record": {
      "comment_id": "U25-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 4565,
            "latency_s": 1.194513,
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
                "guess": 0.05,
                "question": 0.95
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.01,
                  "hit": 0.01
                }
              },
              "C": 0.42,
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
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "completion_tokens": 307,
            "finish_reason": "stop",
            "latency_s": 3.443606,
            "model": "gpt-6-luna",
            "prompt_tokens": 3259,
            "reasoning_tokens": 225
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "家族が約束自体を知っていたかは、真相・確定事実から判断できません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 99,
          "latency_s": 1.66224,
          "model": "gpt-6-luna",
          "prompt_tokens": 1430,
          "reasoning_tokens": 66,
          "slot": "判定語 + 復唱"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "男の家族は二人の約束を知っていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.194861690979451,
      "judge_s": 3.4436595130246133,
      "luna_s": 3.4436595130246133,
      "total_s": 5.106593576958403,
      "writer_s": 1.6629340639337897
    }
  },
  {
    "case_id": "U25-e10",
    "record": {
      "comment_id": "U25-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "no",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "input_tokens": 2321,
            "latency_s": 0.586672,
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
                "point_0": {
                  "close": 0.49,
                  "hit": 0.04
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.04"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 533,
            "finish_reason": "stop",
            "latency_s": 5.830622,
            "model": "gpt-6-luna",
            "prompt_tokens": 3261,
            "reasoning_tokens": 460
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "到着順が勝敗を左右した事実はなく、質問への答えは否定です。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 69,
          "latency_s": 1.293754,
          "model": "gpt-6-luna",
          "prompt_tokens": 1431,
          "reasoning_tokens": 39,
          "slot": "判定語 + 一言"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "勝ったのは、年賀状が先に届いたからなんでしょか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.5868691368959844,
      "judge_s": 5.8306513980496675,
      "luna_s": 5.8306513980496675,
      "total_s": 7.125458523980342,
      "writer_s": 1.2948071259306744
    }
  },
  {
    "case_id": "U25-e11",
    "record": {
      "comment_id": "U25-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 2141,
            "latency_s": 0.57821,
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
                "guess": 0.93,
                "question": 0.07
              },
              "A2": {
                "q_multi": 0.99,
                "q_open": 0.0,
                "q_yesno": 0.01
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
            "completion_tokens": 203,
            "finish_reason": "stop",
            "latency_s": 2.586343,
            "model": "gpt-6-luna",
            "prompt_tokens": 3265,
            "reasoning_tokens": 126
          },
          "error": null,
          "kind": "q_multi",
          "reason": "勝負の開始時期と決着について、質問が二つあるため。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 81,
          "latency_s": 1.805325,
          "model": "gpt-6-luna",
          "prompt_tokens": 1435,
          "reasoning_tokens": 42,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問は一つずつコメントしてね。まずはどちらか聞いてごらん☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "二人は中学のころに勝負したの？その勝負の決着がついたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.5783376399194822,
      "judge_s": 2.5864153769798577,
      "luna_s": 2.5864153769798577,
      "total_s": 4.392702776938677,
      "writer_s": 1.8062873999588192
    }
  },
  {
    "case_id": "U25-e12",
    "record": {
      "comment_id": "U25-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 2147,
            "latency_s": 0.736568,
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
                "guess": 0.2,
                "question": 0.8
              },
              "A2": {
                "q_multi": 0.98,
                "q_open": 0.0,
                "q_yesno": 0.02
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
            "completion_tokens": 127,
            "finish_reason": "stop",
            "latency_s": 2.09102,
            "model": "gpt-6-luna",
            "prompt_tokens": 3264,
            "reasoning_tokens": 55
          },
          "error": null,
          "kind": "q_multi",
          "reason": "年賀状の期間と今年の内容について、質問が二つあります。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 114,
          "latency_s": 2.107592,
          "model": "gpt-6-luna",
          "prompt_tokens": 1434,
          "reasoning_tokens": 74,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。まずはどちらか聞いてごらん☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "年賀状は何十年も送り合ってたの？今年だけ特別な内容だったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.736742147943005,
      "judge_s": 2.0910463489126414,
      "luna_s": 2.0910463489126414,
      "total_s": 4.205088893999346,
      "writer_s": 2.114042545086704
    }
  },
  {
    "case_id": "U25-e13",
    "record": {
      "comment_id": "U25-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 2614,
            "latency_s": 0.733323,
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
                "guess": 0.07,
                "question": 0.93
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.99,
                "q_yesno": 0.01
              },
              "A3": 0.03,
              "A_bare": 0.03
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.03"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 330,
            "finish_reason": "stop",
            "latency_s": 4.763191,
            "model": "gpt-6-luna",
            "prompt_tokens": 3254,
            "reasoning_tokens": 241
          },
          "error": null,
          "kind": "q_open",
          "reason": "「何の勝負」は答えが複数あり、はい・いいえでは答えられない質問です。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 128,
          "latency_s": 2.432861,
          "model": "gpt-6-luna",
          "prompt_tokens": 1424,
          "reasoning_tokens": 90,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は何の勝負に勝ったんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.7336857659975067,
      "judge_s": 4.763239081017673,
      "luna_s": 4.763239081017673,
      "total_s": 7.1971035179449245,
      "writer_s": 2.4338644369272515
    }
  },
  {
    "case_id": "U25-e14",
    "record": {
      "comment_id": "U25-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 2630,
            "latency_s": 0.76157,
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
                "guess": 0.11,
                "question": 0.89
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 1.0,
                "q_yesno": 0.0
              },
              "A3": 0.04,
              "A_bare": 0.04
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
            "completion_tokens": 282,
            "finish_reason": "stop",
            "latency_s": 3.495371,
            "model": "gpt-6-luna",
            "prompt_tokens": 3254,
            "reasoning_tokens": 198
          },
          "error": null,
          "kind": "q_open",
          "reason": "年賀状に何が書かれていたかを尋ねる、はい／いいえで答えられない質問です。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 257,
          "latency_s": 3.305913,
          "model": "gpt-6-luna",
          "prompt_tokens": 1424,
          "reasoning_tokens": 209,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "年賀状に何が書いてあったか、はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "年賀状には何が書いてあったんでしょう？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.7617262080311775,
      "judge_s": 3.4954234010074288,
      "luna_s": 3.4954234010074288,
      "total_s": 6.801946949097328,
      "writer_s": 3.306523548089899
    }
  },
  {
    "case_id": "U25-e15",
    "record": {
      "comment_id": "U25-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 2658,
            "latency_s": 1.365247,
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
                "guess": 0.15,
                "question": 0.85
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.98,
                "q_yesno": 0.02
              },
              "A3": 0.05,
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.05"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 222,
            "finish_reason": "stop",
            "latency_s": 2.828017,
            "model": "gpt-6-luna",
            "prompt_tokens": 3262,
            "reasoning_tokens": 138
          },
          "error": null,
          "kind": "q_open",
          "reason": "どんな約束かを尋ねる質問で、はい・いいえでは答えられません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 135,
          "latency_s": 2.525673,
          "model": "gpt-6-luna",
          "prompt_tokens": 1432,
          "reasoning_tokens": 97,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形にして、聞いてみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "二人は中学を卒業するとき、どんな約束をしたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.365458833053708,
      "judge_s": 2.828047433984466,
      "luna_s": 2.828047433984466,
      "total_s": 5.354668466025032,
      "writer_s": 2.526621032040566
    }
  },
  {
    "case_id": "U25-e16",
    "record": {
      "comment_id": "U25-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 3615,
            "latency_s": 0.724642,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 172,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.99,
                "question": 0.01
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.92,
                  "hit": 0.89
                }
              },
              "B2": 0.08
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.89, 矛盾=0.08"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 229,
            "finish_reason": "stop",
            "latency_s": 2.780886,
            "model": "gpt-6-luna",
            "prompt_tokens": 3264,
            "reasoning_tokens": 131
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "年賀状で将棋を一手ずつ続けたという核心を当てています。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！2人は年賀状に将棋を1手ずつ書き、55年かけて1局を指していた。友人の年賀状に「参りました」とあり、男が勝った。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "2人は年賀状で将棋を一手ずつ指し続けてたってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.7249071759870276,
      "judge_s": 2.7809526269556955,
      "luna_s": 2.7809526269556955,
      "total_s": 2.780967509956099,
      "writer_s": 1.4883000403642654e-05
    }
  },
  {
    "case_id": "U25-e17",
    "record": {
      "comment_id": "U25-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 3731,
            "latency_s": 0.818196,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 172,
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
                "point_0": {
                  "close": 0.99,
                  "hit": 0.98
                }
              },
              "B2": 0.06
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.98, 矛盾=0.06"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 287,
            "finish_reason": "stop",
            "latency_s": 3.255645,
            "model": "gpt-6-luna",
            "prompt_tokens": 3288,
            "reasoning_tokens": 178
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "年賀状で将棋を一手ずつ指し、55年目に友人が投了した核心を説明しています。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！2人は年賀状に将棋を1手ずつ書き、55年かけて1局を指していた。友人の年賀状に「参りました」とあり、男が勝った。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "会えないまま、2人は年賀状で将棋を一手ずつ続けてたんだね。55年越しに相手が「参りました」と送ってきたのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.8184982299571857,
      "judge_s": 3.2557222879258916,
      "luna_s": 3.2557222879258916,
      "total_s": 3.255728045012802,
      "writer_s": 5.757086910307407e-06
    }
  },
  {
    "case_id": "U25-e18",
    "record": {
      "comment_id": "U25-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 2324,
            "latency_s": 0.594745,
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
                "point_0": {
                  "close": 0.98,
                  "hit": 0.02
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.02"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 128,
            "finish_reason": "stop",
            "latency_s": 2.594883,
            "model": "gpt-6-luna",
            "prompt_tokens": 3265,
            "reasoning_tokens": 58
          },
          "error": null,
          "kind": "guess_close",
          "reason": "年賀状で勝負を続けた点には触れていますが、将棋を指していたとは特定できていません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 77,
          "latency_s": 1.954907,
          "model": "gpt-6-luna",
          "prompt_tokens": 1435,
          "reasoning_tokens": 44,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！ほかの可能性も考えてみようか☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "2人は年賀状で何かの勝負をずっと続けてたんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.5950343071017414,
      "judge_s": 2.594950931961648,
      "luna_s": 2.594950931961648,
      "total_s": 4.550758188939653,
      "writer_s": 1.9558072569780052
    }
  },
  {
    "case_id": "U25-e19",
    "record": {
      "comment_id": "U25-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "calls": 4,
            "input_tokens": 3687,
            "latency_s": 0.799101,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 172,
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
                "point_0": {
                  "close": 0.92,
                  "hit": 0.88
                }
              },
              "B2": 0.98
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.88, 矛盾=0.98"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 184,
            "finish_reason": "stop",
            "latency_s": 2.935012,
            "model": "gpt-6-luna",
            "prompt_tokens": 3281,
            "reasoning_tokens": 120
          },
          "error": null,
          "kind": "guess_close",
          "reason": "年賀状で将棋を指した点は合っていますが、毎年会ったという誤りがあります。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 130,
          "latency_s": 2.366615,
          "model": "gpt-6-luna",
          "prompt_tokens": 1451,
          "reasoning_tokens": 101,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "年賀状で将棋を一手ずつ続けてたけど、2人は毎年会って、その場で次の手を決めてたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.7993553120177239,
      "judge_s": 2.9350432769861072,
      "luna_s": 2.9350432769861072,
      "total_s": 5.302796295960434,
      "writer_s": 2.3677530189743266
    }
  },
  {
    "case_id": "U25-e20",
    "record": {
      "comment_id": "U25-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 4721,
            "latency_s": 1.256839,
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
                "q_multi": 0.02,
                "q_open": 0.39,
                "q_yesno": 0.59
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.39,
              "D": {
                "irrelevant": 0.01,
                "no": 0.99,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 405,
            "finish_reason": "stop",
            "latency_s": 4.892092,
            "model": "gpt-6-luna",
            "prompt_tokens": 3283,
            "reasoning_tokens": 334
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "年賀状で続けた勝負に触れておらず、賭けは確定事実とも異なります。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 30,
          "latency_s": 1.881635,
          "model": "gpt-6-luna",
          "prompt_tokens": 1453,
          "reasoning_tokens": 0,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。別の可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "中学の時にどっちが先に結婚するか賭けていて、友人が独身だとわかったから勝ちを喜んだんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.2570868469774723,
      "judge_s": 4.892167604062706,
      "luna_s": 4.892167604062706,
      "total_s": 6.7743872629944235,
      "writer_s": 1.8822196589317173
    }
  },
  {
    "case_id": "U25-e21",
    "record": {
      "comment_id": "U25-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "calls": 4,
            "guess_demoted": true,
            "input_tokens": 2913,
            "latency_s": 0.891404,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 194,
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
                "q_multi": 0.02,
                "q_open": 0.86,
                "q_yesno": 0.12
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.23,
                  "hit": 0.03
                }
              }
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.03"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 245,
            "finish_reason": "stop",
            "latency_s": 3.173175,
            "model": "gpt-6-luna",
            "prompt_tokens": 3274,
            "reasoning_tokens": 178
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "年賀状での宝くじ当選や賭けは、勝負の仕掛けではありません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 31,
          "latency_s": 2.62076,
          "model": "gpt-6-luna",
          "prompt_tokens": 1444,
          "reasoning_tokens": 0,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "友人が年賀状で宝くじが当たったと知らせてきて、昔の賭けに勝ったんだと思う。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.8915695160394534,
      "judge_s": 3.173216459923424,
      "luna_s": 3.173216459923424,
      "total_s": 5.795145508949645,
      "writer_s": 2.621929049026221
    }
  },
  {
    "case_id": "U25-k01",
    "record": {
      "comment_id": "U25-k01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 3663,
            "latency_s": 0.74342,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 172,
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
                "point_0": {
                  "close": 0.9700000000000001,
                  "hit": 0.92
                }
              },
              "B2": 0.08
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.92, 矛盾=0.08"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 265,
            "finish_reason": "stop",
            "latency_s": 2.975338,
            "model": "gpt-6-luna",
            "prompt_tokens": 3276,
            "reasoning_tokens": 160
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "年賀状で将棋を一手ずつ続けたという核心を正しく当てています。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！2人は年賀状に将棋を1手ずつ書き、55年かけて1局を指していた。友人の年賀状に「参りました」とあり、男が勝った。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "新年の便りに盤面の次の手を書き添えて、二人は将棋を何十年も続けてたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.7435686819953844,
      "judge_s": 2.975457667023875,
      "luna_s": 2.975457667023875,
      "total_s": 2.975472514051944,
      "writer_s": 1.4847028069198132e-05
    }
  },
  {
    "case_id": "U25-k02",
    "record": {
      "comment_id": "U25-k02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 2357,
            "latency_s": 0.710417,
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
              "A_bare": 0.03,
              "B": {
                "point_0": {
                  "close": 0.8999999999999999,
                  "hit": 0.29
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.29"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 191,
            "finish_reason": "stop",
            "latency_s": 2.707749,
            "model": "gpt-6-luna",
            "prompt_tokens": 3274,
            "reasoning_tokens": 122
          },
          "error": null,
          "kind": "guess_close",
          "reason": "年始のはがきで一手ずつ対局した点は触れていますが、将棋とは特定していません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 76,
          "latency_s": 1.867207,
          "model": "gpt-6-luna",
          "prompt_tokens": 1444,
          "reasoning_tokens": 43,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！ほかの可能性も考えてみようか☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "離れて暮らす二人が、年始のはがきで一手ずつ棋譜をつなぐ対局だったんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.710668025072664,
      "judge_s": 2.707794312038459,
      "luna_s": 2.707794312038459,
      "total_s": 4.575598035007715,
      "writer_s": 1.8678037229692563
    }
  },
  {
    "case_id": "U25-k03",
    "record": {
      "comment_id": "U25-k03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 2330,
            "latency_s": 0.62393,
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
              "A_bare": 0.03,
              "B": {
                "point_0": {
                  "close": 0.97,
                  "hit": 0.02
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.02"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 150,
            "finish_reason": "stop",
            "latency_s": 2.454838,
            "model": "gpt-6-luna",
            "prompt_tokens": 3266,
            "reasoning_tokens": 78
          },
          "error": null,
          "kind": "guess_close",
          "reason": "年賀状で勝負を続けた点には触れていますが、将棋を一手ずつ指したとは特定していません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 82,
          "latency_s": 2.522119,
          "model": "gpt-6-luna",
          "prompt_tokens": 1436,
          "reasoning_tokens": 49,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し推理を続けてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "年賀状を通して二人は長く何かの勝負を続けていたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.6241571290884167,
      "judge_s": 2.4548856269102544,
      "luna_s": 2.4548856269102544,
      "total_s": 4.977880010963418,
      "writer_s": 2.5229943840531632
    }
  },
  {
    "case_id": "U25-k04",
    "record": {
      "comment_id": "U25-k04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "calls": 4,
            "input_tokens": 3691,
            "latency_s": 0.881864,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 172,
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
                "point_0": {
                  "close": 0.86,
                  "hit": 0.64
                }
              },
              "B2": 0.97
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.64, 矛盾=0.97"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 147,
            "finish_reason": "stop",
            "latency_s": 2.268604,
            "model": "gpt-6-luna",
            "prompt_tokens": 3279,
            "reasoning_tokens": 77
          },
          "error": null,
          "kind": "guess_close",
          "reason": "年賀状で将棋を続けた点は合っていますが、毎年顔を合わせた点が真相と異なります。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 24,
          "latency_s": 2.296557,
          "model": "gpt-6-luna",
          "prompt_tokens": 1449,
          "reasoning_tokens": 0,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！推理を続けてみようか😉"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "新年のはがきで将棋の続きを送り合ってたけど、二人は毎年顔を合わせて次の手を決めてたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.8820967089850456,
      "judge_s": 2.2686567819910124,
      "luna_s": 2.2686567819910124,
      "total_s": 4.565498474985361,
      "writer_s": 2.2968416929943487
    }
  },
  {
    "case_id": "U25-k05",
    "record": {
      "comment_id": "U25-k05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 2351,
            "latency_s": 0.659518,
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
                "point_0": {
                  "close": 0.99,
                  "hit": 0.02
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.02"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 233,
            "finish_reason": "stop",
            "latency_s": 3.230104,
            "model": "gpt-6-luna",
            "prompt_tokens": 3272,
            "reasoning_tokens": 166
          },
          "error": null,
          "kind": "guess_close",
          "reason": "年賀状で勝負を続けていた点には触れていますが、核心までは特定できていません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 96,
          "latency_s": 2.249208,
          "model": "gpt-6-luna",
          "prompt_tokens": 1442,
          "reasoning_tokens": 67,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "年賀状には勝負の続きが記され、二人は毎年やりとりを重ねていたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.6598655129782856,
      "judge_s": 3.2301461870083585,
      "luna_s": 3.2301461870083585,
      "total_s": 5.479728281963617,
      "writer_s": 2.249582094955258
    }
  },
  {
    "case_id": "U25-k06",
    "record": {
      "comment_id": "U25-k06",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "calls": 4,
            "guess_demoted": true,
            "input_tokens": 2897,
            "latency_s": 0.779959,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 194,
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
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.88,
                "q_yesno": 0.11
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              }
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.00"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 177,
            "finish_reason": "stop",
            "latency_s": 2.522749,
            "model": "gpt-6-luna",
            "prompt_tokens": 3271,
            "reasoning_tokens": 107
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "中学時代を思い出したというだけで、年賀状で続けた勝負に触れていません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 31,
          "latency_s": 2.115314,
          "model": "gpt-6-luna",
          "prompt_tokens": 1441,
          "reasoning_tokens": 0,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "友人は年賀状で、55年ぶりに中学時代の話を思い出したと知らせたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.7802765039959922,
      "judge_s": 2.5228412179276347,
      "luna_s": 2.5228412179276347,
      "total_s": 4.643772177980281,
      "writer_s": 2.1209309600526467
    }
  },
  {
    "case_id": "U25-t01",
    "record": {
      "comment_id": "U25-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "年賀状将棋",
          "debug": {
            "calls": 1,
            "input_tokens": 930,
            "latency_s": 0.208222,
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
              "A_bare": 0.86
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.86"
        },
        "luna": {
          "answer": null,
          "bare_term": "年賀状将棋",
          "debug": {
            "completion_tokens": 167,
            "finish_reason": "stop",
            "latency_s": 2.486297,
            "model": "gpt-6-luna",
            "prompt_tokens": 3247,
            "reasoning_tokens": 90
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句だけのコメントなので、推理ではなく質問として扱います。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "年賀状将棋がどうしたのか聞かせてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "年賀状将棋？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.20832316600717604,
      "judge_s": 2.486330740037374,
      "luna_s": 2.486330740037374,
      "total_s": 6.222630903124809,
      "writer_s": 3.736300163087435
    }
  },
  {
    "case_id": "U25-t02",
    "record": {
      "comment_id": "U25-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "野球部",
          "debug": {
            "calls": 1,
            "input_tokens": 927,
            "latency_s": 0.192709,
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
          "bare_term": "野球部",
          "debug": {
            "completion_tokens": 206,
            "finish_reason": "stop",
            "latency_s": 2.543388,
            "model": "gpt-6-luna",
            "prompt_tokens": 3244,
            "reasoning_tokens": 113
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句だけのコメントなので、質問として聞き直しを促します。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "何が野球部なのか教えてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "野球部",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.19282692996785045,
      "judge_s": 2.5434504689183086,
      "luna_s": 2.5434504689183086,
      "total_s": 5.720738842966966,
      "writer_s": 3.1772883740486577
    }
  },
  {
    "case_id": "c-ask_howto-01",
    "record": {
      "comment_id": "c-ask_howto-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "input_tokens": 1427,
            "latency_s": 0.376599,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 124,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.01,
                "reaction": 0.0,
                "request": 0.99
              },
              "A2": {
                "ask_hint": 0.0,
                "ask_howto": 1.0,
                "ask_spoiler": 0.0
              },
              "A_bare": 0.04
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
            "completion_tokens": 192,
            "finish_reason": "stop",
            "latency_s": 2.437016,
            "model": "gpt-6-luna",
            "prompt_tokens": 3249,
            "reasoning_tokens": 120
          },
          "error": null,
          "kind": "ask_howto",
          "reason": "遊び方を尋ねているコメントです。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 37,
          "latency_s": 1.284283,
          "model": "gpt-6-luna",
          "prompt_tokens": 1421,
          "reasoning_tokens": 0,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる質問をコメントすると、探偵が答えるよ！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "これどうやって遊ぶの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.37674521293956786,
      "judge_s": 2.437073520035483,
      "luna_s": 2.437073520035483,
      "total_s": 3.722119939979166,
      "writer_s": 1.2850464199436828
    }
  },
  {
    "case_id": "c-greeting-05",
    "record": {
      "comment_id": "c-greeting-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "greeting"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1580,
            "latency_s": 0.394628,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 150,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 1.0,
                "request": 0.0
              },
              "A2": {
                "chat": 0.0,
                "cheer": 0.0,
                "complaint": 0.0,
                "greeting": 1.0,
                "impression": 0.0,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.14
            }
          },
          "error": null,
          "kind": "greeting",
          "reason": "段A=reaction→greeting"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 86,
            "finish_reason": "stop",
            "latency_s": 1.854963,
            "model": "gpt-6-luna",
            "prompt_tokens": 3247,
            "reasoning_tokens": 29
          },
          "error": null,
          "kind": "greeting",
          "reason": "初コメントの挨拶なので、歓迎の返信をします。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 92,
          "latency_s": 1.462734,
          "model": "gpt-6-luna",
          "prompt_tokens": 1416,
          "reasoning_tokens": 67,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "こんにちは！初コメありがとう☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "こんにちは、初コメです",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.3948377389460802,
      "judge_s": 1.8549909909488633,
      "luna_s": 1.8549909909488633,
      "total_s": 3.318742206902243,
      "writer_s": 1.4637512159533799
    }
  },
  {
    "case_id": "c-request-04",
    "record": {
      "comment_id": "c-request-04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "request"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1429,
            "latency_s": 0.390922,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 124,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.26,
                "request": 0.74
              },
              "A2": {
                "ask_hint": 0.27,
                "ask_howto": 0.66,
                "ask_spoiler": 0.07
              },
              "A_bare": 0.53
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
            "completion_tokens": 155,
            "finish_reason": "stop",
            "latency_s": 2.392171,
            "model": "gpt-6-luna",
            "prompt_tokens": 3250,
            "reasoning_tokens": 100
          },
          "error": null,
          "kind": "request",
          "reason": "短めの問題を求めるリクエストです。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 69,
          "latency_s": 1.450901,
          "model": "gpt-6-luna",
          "prompt_tokens": 1419,
          "reasoning_tokens": 46,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "リクエストありがとう！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "短めの問題リクエストです",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.3910408769734204,
      "judge_s": 2.392351416987367,
      "luna_s": 2.392351416987367,
      "total_s": 3.8442234250251204,
      "writer_s": 1.4518720080377534
    }
  },
  {
    "case_id": "c-emoji_only-03",
    "record": {
      "comment_id": "c-emoji_only-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "emoji_only"
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
          "kind": "emoji_only",
          "reason": "段0規則: emoji_only"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 160,
            "finish_reason": "stop",
            "latency_s": 2.443758,
            "model": "gpt-6-luna",
            "prompt_tokens": 3243,
            "reasoning_tokens": 107
          },
          "error": null,
          "kind": "emoji_only",
          "reason": "絵文字だけのコメントなので、emoji_onlyに分類します。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 86,
          "latency_s": 1.745769,
          "model": "gpt-6-luna",
          "prompt_tokens": 1413,
          "reasoning_tokens": 59,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "おっ、びっくりだね！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "😮",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 3.6587007343769073e-05,
      "judge_s": 2.443822061060928,
      "luna_s": 2.443822061060928,
      "total_s": 4.190597407054156,
      "writer_s": 1.7467753459932283
    }
  },
  {
    "case_id": "c-spam-02",
    "record": {
      "comment_id": "c-spam-02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
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
            "calls": 2,
            "input_tokens": 1484,
            "latency_s": 0.38402,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 128,
            "probabilities": {
              "A1": {
                "inappropriate": 1.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A2": {
                "abuse": 0.0,
                "personal_info": 0.0,
                "spam": 1.0,
                "troll": 0.0
              },
              "A_bare": 0.03
            }
          },
          "error": null,
          "kind": "spam",
          "reason": "段A=inappropriate→spam"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 73,
            "finish_reason": "stop",
            "latency_s": 1.645527,
            "model": "gpt-6-luna",
            "prompt_tokens": 3252,
            "reasoning_tokens": 28
          },
          "error": null,
          "kind": "spam",
          "reason": "フォロー交換を促す宣伝コメントです。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "no_reply",
        "text": null
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "フォローしてくれたら相互します！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.3841622010804713,
      "judge_s": 1.6455797540256754,
      "luna_s": 1.6455797540256754,
      "total_s": 1.645584108075127,
      "writer_s": 4.354049451649189e-06
    }
  },
  {
    "case_id": "c-abuse-06",
    "record": {
      "comment_id": "c-abuse-06",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "abuse"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1480,
            "latency_s": 0.38497,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
            "probabilities": {
              "A1": {
                "inappropriate": 0.87,
                "other": 0.0,
                "question_or_guess": 0.11,
                "reaction": 0.02,
                "request": 0.0
              },
              "A2": {
                "abuse": 1.0,
                "personal_info": 0.0,
                "spam": 0.0,
                "troll": 0.0
              },
              "A_bare": 0.05
            }
          },
          "error": null,
          "kind": "abuse",
          "reason": "段A=inappropriate→abuse"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 108,
            "finish_reason": "stop",
            "latency_s": 2.007059,
            "model": "gpt-6-luna",
            "prompt_tokens": 3252,
            "reasoning_tokens": 61
          },
          "error": null,
          "kind": "abuse",
          "reason": "問題ではなく作者本人をけなす内容です。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "ここではやさしい言葉でお願いね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "作者って絶対友達いないでしょ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.38512119092047215,
      "judge_s": 2.0070884249871597,
      "luna_s": 2.0070884249871597,
      "total_s": 2.0071265269070864,
      "writer_s": 3.8101919926702976e-05
    }
  }
];
