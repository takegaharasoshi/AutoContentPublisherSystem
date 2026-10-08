window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["dec-2c/U25"] = [
  {
    "case_id": "U25-e01",
    "record": {
      "comment_id": "U25-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "no",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.02
              },
              "A2": {
                "kind": 0.97
              },
              "B": {
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.97
              }
            },
            "input_tokens": 3178,
            "latency_s": 1.531642,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.51,
                "question": 0.49
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.01,
                "q_yesno": 0.98
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.63,
              "D": {
                "irrelevant": 0.01,
                "no": 0.98,
                "yes": 0.01
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 82,
          "latency_s": 1.892668,
          "model": "gpt-6-luna",
          "prompt_tokens": 1431,
          "reasoning_tokens": 52,
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
      "shadow_mismatch": null,
      "text": "中学時代に二人で何か賭けをしてたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.5318541949382052,
      "jev_s": null,
      "judge_s": 1.5318541949382052,
      "luna_s": null,
      "total_s": 3.425077651045285,
      "writer_s": 1.89322345610708
    }
  },
  {
    "case_id": "U25-e02",
    "record": {
      "comment_id": "U25-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "yes",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.94
              },
              "A2": {
                "kind": 0.97
              },
              "B": {
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.99
              }
            },
            "input_tokens": 3172,
            "latency_s": 2.730091,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_multi": 0.01,
                "q_open": 0.01,
                "q_yesno": 0.98
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.55,
              "D": {
                "irrelevant": 0.0,
                "no": 0.01,
                "yes": 0.99
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 27,
          "latency_s": 1.544397,
          "model": "gpt-6-luna",
          "prompt_tokens": 1428,
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
      "shadow_mismatch": null,
      "text": "「勝った」は、昔した勝負の結果について言ってるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 2.730495902011171,
      "jev_s": null,
      "judge_s": 2.730495902011171,
      "luna_s": null,
      "total_s": 4.306689454941079,
      "writer_s": 1.576193552929908
    }
  },
  {
    "case_id": "U25-e03",
    "record": {
      "comment_id": "U25-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "yes",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 0.99
              },
              "A1b": {
                "qg": 0.98
              },
              "A2": {
                "kind": 0.97
              },
              "B": {
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.97
              }
            },
            "input_tokens": 3178,
            "latency_s": 1.364111,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.0,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.01,
                "question": 0.99
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.01,
                "q_yesno": 0.98
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.49,
              "D": {
                "irrelevant": 0.0,
                "no": 0.02,
                "yes": 0.98
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 30,
          "latency_s": 1.225628,
          "model": "gpt-6-luna",
          "prompt_tokens": 1429,
          "reasoning_tokens": 11,
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
      "shadow_mismatch": null,
      "text": "友人は毎年ずっと年賀状を送り続けていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.364439224009402,
      "jev_s": null,
      "judge_s": 1.364439224009402,
      "luna_s": null,
      "total_s": 2.590760964085348,
      "writer_s": 1.2263217400759459
    }
  },
  {
    "case_id": "U25-e04",
    "record": {
      "comment_id": "U25-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "yes",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.98
              },
              "A2": {
                "kind": 0.97
              },
              "B": {
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 1.0
              }
            },
            "input_tokens": 3130,
            "latency_s": 1.466272,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_multi": 0.01,
                "q_open": 0.01,
                "q_yesno": 0.98
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.92,
              "D": {
                "irrelevant": 0.0,
                "no": 0.0,
                "yes": 1.0
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 13,
          "latency_s": 1.019676,
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
      "shadow_mismatch": null,
      "text": "二人は中学の同級生ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.4665646679932252,
      "jev_s": null,
      "judge_s": 1.4665646679932252,
      "luna_s": null,
      "total_s": 2.486982294009067,
      "writer_s": 1.020417626015842
    }
  },
  {
    "case_id": "U25-e05",
    "record": {
      "comment_id": "U25-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "yes",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.02
              },
              "A2": {
                "kind": 1.0
              },
              "B": {
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.53
              }
            },
            "input_tokens": 3166,
            "latency_s": 1.791293,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.51,
                "question": 0.49
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.94,
              "D": {
                "irrelevant": 0.02,
                "no": 0.29,
                "yes": 0.69
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 37,
          "latency_s": 1.193495,
          "model": "gpt-6-luna",
          "prompt_tokens": 1427,
          "reasoning_tokens": 18,
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
      "shadow_mismatch": null,
      "text": "年賀状に勝負の答えが書かれていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.7917322389548644,
      "jev_s": null,
      "judge_s": 1.7917322389548644,
      "luna_s": null,
      "total_s": 2.9860248549375683,
      "writer_s": 1.1942926159827039
    }
  },
  {
    "case_id": "U25-e06",
    "record": {
      "comment_id": "U25-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "yes",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.86
              },
              "A2": {
                "kind": 0.99
              },
              "B": {
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.43
              }
            },
            "input_tokens": 3172,
            "latency_s": 1.747184,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_multi": 0.01,
                "q_open": 0.0,
                "q_yesno": 0.99
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.44,
              "D": {
                "irrelevant": 0.08,
                "no": 0.3,
                "yes": 0.62
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 134,
          "latency_s": 2.051548,
          "model": "gpt-6-luna",
          "prompt_tokens": 1431,
          "reasoning_tokens": 96,
          "slot": "判定語 + 復唱"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！男は友人がまだ生きているか気にしていたんだね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は友人がまだ生きているか気にしていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.7476008959347382,
      "jev_s": null,
      "judge_s": 1.7476008959347382,
      "luna_s": null,
      "total_s": 3.7998503339476883,
      "writer_s": 2.05224943801295
    }
  },
  {
    "case_id": "U25-e07",
    "record": {
      "comment_id": "U25-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "yes",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.98
              },
              "A2": {
                "kind": 0.99
              },
              "B": {
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.79
              }
            },
            "input_tokens": 3160,
            "latency_s": 1.536743,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.71,
              "D": {
                "irrelevant": 0.01,
                "no": 0.13,
                "yes": 0.86
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 117,
          "latency_s": 2.047404,
          "model": "gpt-6-luna",
          "prompt_tokens": 1429,
          "reasoning_tokens": 81,
          "slot": "判定語 + 復唱"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！二人とも元日に年賀状を受け取ったんだね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "二人とも元日に年賀状を受け取ったんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.53705149597954,
      "jev_s": null,
      "judge_s": 1.53705149597954,
      "luna_s": null,
      "total_s": 3.596335323061794,
      "writer_s": 2.059283827082254
    }
  },
  {
    "case_id": "U25-e08",
    "record": {
      "comment_id": "U25-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "yes",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 1.0
              },
              "A2": {
                "kind": 0.99
              },
              "B": {
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.77
              }
            },
            "input_tokens": 3148,
            "latency_s": 1.36123,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.0,
                "question": 1.0
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.0,
                "q_yesno": 0.99
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.61,
              "D": {
                "irrelevant": 0.08,
                "no": 0.07,
                "yes": 0.85
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 143,
          "latency_s": 2.398947,
          "model": "gpt-6-luna",
          "prompt_tokens": 1427,
          "reasoning_tokens": 109,
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
      "shadow_mismatch": null,
      "text": "友人は男と同じくらいの年齢ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.3615592999849468,
      "jev_s": null,
      "judge_s": 1.3615592999849468,
      "luna_s": null,
      "total_s": 3.7611866539809853,
      "writer_s": 2.3996273539960384
    }
  },
  {
    "case_id": "U25-e09",
    "record": {
      "comment_id": "U25-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "yes",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 1.0
              },
              "A2": {
                "kind": 0.99
              },
              "B": {
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.99
              }
            },
            "input_tokens": 3166,
            "latency_s": 1.317531,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.0,
                "question": 1.0
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.73,
              "D": {
                "irrelevant": 0.0,
                "no": 0.01,
                "yes": 0.99
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 159,
          "latency_s": 2.086878,
          "model": "gpt-6-luna",
          "prompt_tokens": 1430,
          "reasoning_tokens": 122,
          "slot": "判定語 + 復唱"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！男の家族は二人の約束を知っていたんですか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男の家族は二人の約束を知っていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.3178421690827236,
      "jev_s": null,
      "judge_s": 1.3178421690827236,
      "luna_s": null,
      "total_s": 3.4058378550689667,
      "writer_s": 2.087995685986243
    }
  },
  {
    "case_id": "U25-e10",
    "record": {
      "comment_id": "U25-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 5,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.68
              },
              "A2": {
                "kind": 0.79
              },
              "B": {
                "point_0": 1.0
              },
              "C": {}
            },
            "input_tokens": 2333,
            "latency_s": 1.140843,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_multi": 0.01,
                "q_open": 0.13,
                "q_yesno": 0.86
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.03
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 201,
          "latency_s": 3.029136,
          "model": "gpt-6-luna",
          "prompt_tokens": 1431,
          "reasoning_tokens": 163,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞き直してみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "勝ったのは、年賀状が先に届いたからなんでしょか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.1410468450048938,
      "jev_s": null,
      "judge_s": 1.1410468450048938,
      "luna_s": null,
      "total_s": 4.171063245041296,
      "writer_s": 3.030016400036402
    }
  },
  {
    "case_id": "U25-e11",
    "record": {
      "comment_id": "U25-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_multi"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "confidence": {
              "A1": {
                "major": 0.99
              },
              "A1b": {
                "qg": 0.98
              },
              "A2": {
                "kind": 0.53
              }
            },
            "input_tokens": 1511,
            "latency_s": 0.759812,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.0,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.01,
                "question": 0.99
              },
              "A2": {
                "q_multi": 0.69,
                "q_open": 0.02,
                "q_yesno": 0.29
              },
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_multi",
          "reason": "段A=question→q_multi"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 77,
          "latency_s": 1.413627,
          "model": "gpt-6-luna",
          "prompt_tokens": 1435,
          "reasoning_tokens": 40,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつ聞いてごらん。順番に答えるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "二人は中学のころに勝負したの？その勝負の決着がついたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.7600090020569041,
      "jev_s": null,
      "judge_s": 0.7600090020569041,
      "luna_s": null,
      "total_s": 2.174651324050501,
      "writer_s": 1.4146423219935969
    }
  },
  {
    "case_id": "U25-e12",
    "record": {
      "comment_id": "U25-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_multi"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 1.0
              },
              "A2": {
                "kind": 0.79
              }
            },
            "input_tokens": 1508,
            "latency_s": 0.661625,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.0,
                "question": 1.0
              },
              "A2": {
                "q_multi": 0.86,
                "q_open": 0.01,
                "q_yesno": 0.13
              },
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_multi",
          "reason": "段A=question→q_multi"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 72,
          "latency_s": 5.661095,
          "model": "gpt-6-luna",
          "prompt_tokens": 1434,
          "reasoning_tokens": 32,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつしてごらん。どっちから聞こうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "年賀状は何十年も送り合ってたの？今年だけ特別な内容だったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.6618918599560857,
      "jev_s": null,
      "judge_s": 0.6618918599560857,
      "luna_s": null,
      "total_s": 6.329711430938914,
      "writer_s": 5.667819570982829
    }
  },
  {
    "case_id": "U25-e13",
    "record": {
      "comment_id": "U25-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.98
              },
              "A2": {
                "kind": 0.89
              },
              "A3": {}
            },
            "input_tokens": 1835,
            "latency_s": 0.932779,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_multi": 0.01,
                "q_open": 0.93,
                "q_yesno": 0.06
              },
              "A3": 0.0,
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 90,
          "latency_s": 2.204635,
          "model": "gpt-6-luna",
          "prompt_tokens": 1424,
          "reasoning_tokens": 50,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はいかいいえで答えられる形にして、聞き直してみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は何の勝負に勝ったんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9329472390236333,
      "jev_s": null,
      "judge_s": 0.9329472390236333,
      "luna_s": null,
      "total_s": 3.1386023530503735,
      "writer_s": 2.20565511402674
    }
  },
  {
    "case_id": "U25-e14",
    "record": {
      "comment_id": "U25-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.98
              },
              "A2": {
                "kind": 0.97
              },
              "A3": {}
            },
            "input_tokens": 1835,
            "latency_s": 0.885632,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_multi": 0.01,
                "q_open": 0.98,
                "q_yesno": 0.01
              },
              "A3": 0.0,
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 114,
          "latency_s": 2.508683,
          "model": "gpt-6-luna",
          "prompt_tokens": 1424,
          "reasoning_tokens": 76,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞き直してみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "年賀状には何が書いてあったんでしょう？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.8858007000526413,
      "jev_s": null,
      "judge_s": 0.8858007000526413,
      "luna_s": null,
      "total_s": 3.395628384081647,
      "writer_s": 2.5098276840290055
    }
  },
  {
    "case_id": "U25-e15",
    "record": {
      "comment_id": "U25-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.9
              },
              "A2": {
                "kind": 1.0
              },
              "A3": {}
            },
            "input_tokens": 1867,
            "latency_s": 0.921834,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_open": 1.0,
                "q_yesno": 0.0
              },
              "A3": 0.01,
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 135,
          "latency_s": 2.692324,
          "model": "gpt-6-luna",
          "prompt_tokens": 1432,
          "reasoning_tokens": 98,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "二人は中学卒業のときに約束をしたの？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "二人は中学を卒業するとき、どんな約束をしたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9220235099783167,
      "jev_s": null,
      "judge_s": 0.9220235099783167,
      "luna_s": null,
      "total_s": 3.614787177881226,
      "writer_s": 2.692763667902909
    }
  },
  {
    "case_id": "U25-e16",
    "record": {
      "comment_id": "U25-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_correct"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.92
              },
              "B": {
                "point_0": 0.97
              },
              "B2": {}
            },
            "input_tokens": 2669,
            "latency_s": 0.924204,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.98,
                  "hit": 0.98
                }
              },
              "B2": 0.01
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.98, 矛盾=0.01"
        },
        "jev": null,
        "luna": null
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
      "shadow_mismatch": null,
      "text": "2人は年賀状で将棋を一手ずつ指し続けてたってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.924510975019075,
      "jev_s": null,
      "judge_s": 0.924510975019075,
      "luna_s": null,
      "total_s": 0.9245192939415574,
      "writer_s": 8.318922482430935e-06
    }
  },
  {
    "case_id": "U25-e17",
    "record": {
      "comment_id": "U25-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_correct"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 0.98
              },
              "A1b": {
                "qg": 1.0
              },
              "B": {
                "point_0": 0.99
              },
              "B2": {}
            },
            "input_tokens": 2765,
            "latency_s": 1.00675,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.98,
                "reaction": 0.01,
                "request": 0.01
              },
              "A1b": {
                "guess": 1.0,
                "question": 0.0
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 1.0,
                  "hit": 0.99
                }
              },
              "B2": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.99, 矛盾=0.00"
        },
        "jev": null,
        "luna": null
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
      "shadow_mismatch": null,
      "text": "会えないまま、2人は年賀状で将棋を一手ずつ続けてたんだね。55年越しに相手が「参りました」と送ってきたのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.0070577949518338,
      "jev_s": null,
      "judge_s": 1.0070577949518338,
      "luna_s": null,
      "total_s": 1.0070603749481961,
      "writer_s": 2.5799963623285294e-06
    }
  },
  {
    "case_id": "U25-e18",
    "record": {
      "comment_id": "U25-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_close"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "confidence": {
              "A1": {
                "major": 0.99
              },
              "A1b": {
                "qg": 0.98
              },
              "B": {
                "point_0": 0.97
              }
            },
            "input_tokens": 1672,
            "latency_s": 0.725196,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.0,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.99,
                "question": 0.01
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.98,
                  "hit": 0.0
                }
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 27,
          "latency_s": 1.277998,
          "model": "gpt-6-luna",
          "prompt_tokens": 1435,
          "reasoning_tokens": 0,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し推理を続けてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "2人は年賀状で何かの勝負をずっと続けてたんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.7253918949281797,
      "jev_s": null,
      "judge_s": 0.7253918949281797,
      "luna_s": null,
      "total_s": 2.0142200528644025,
      "writer_s": 1.2888281579362229
    }
  },
  {
    "case_id": "U25-e19",
    "record": {
      "comment_id": "U25-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 0.99
              },
              "A1b": {
                "qg": 0.54
              },
              "A2": {
                "kind": 0.55
              },
              "A3": {}
            },
            "input_tokens": 1943,
            "latency_s": 0.943273,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.01,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.77,
                "question": 0.23
              },
              "A2": {
                "q_multi": 0.08,
                "q_open": 0.7,
                "q_yesno": 0.22
              },
              "A3": 0.03,
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.03"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 106,
          "latency_s": 2.192674,
          "model": "gpt-6-luna",
          "prompt_tokens": 1451,
          "reasoning_tokens": 68,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形にして、聞き直してみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "年賀状で将棋を一手ずつ続けてたけど、2人は毎年会って、その場で次の手を決めてたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9434963340172544,
      "jev_s": null,
      "judge_s": 0.9434963340172544,
      "luna_s": null,
      "total_s": 3.1365404720418155,
      "writer_s": 2.193044138024561
    }
  },
  {
    "case_id": "U25-e20",
    "record": {
      "comment_id": "U25-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_wrong"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 0.99
              },
              "A1b": {
                "qg": 0.94
              },
              "A2": {
                "kind": 0.61
              },
              "B": {
                "point_0": 1.0
              }
            },
            "guess_demoted": true,
            "input_tokens": 2057,
            "latency_s": 0.879054,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.0,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.97,
                "question": 0.03
              },
              "A2": {
                "q_multi": 0.05,
                "q_open": 0.74,
                "q_yesno": 0.21
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 30,
          "latency_s": 1.508301,
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
      "shadow_mismatch": null,
      "text": "中学の時にどっちが先に結婚するか賭けていて、友人が独身だとわかったから勝ちを喜んだんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.8792082449654117,
      "jev_s": null,
      "judge_s": 0.8792082449654117,
      "luna_s": null,
      "total_s": 2.387930896016769,
      "writer_s": 1.5087226510513574
    }
  },
  {
    "case_id": "U25-e21",
    "record": {
      "comment_id": "U25-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_wrong"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 0.99
              },
              "A1b": {
                "qg": 0.98
              },
              "A2": {
                "kind": 0.82
              },
              "B": {
                "point_0": 1.0
              }
            },
            "guess_demoted": true,
            "input_tokens": 2021,
            "latency_s": 0.912153,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.0,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.99,
                "question": 0.01
              },
              "A2": {
                "q_multi": 0.04,
                "q_open": 0.88,
                "q_yesno": 0.08
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 87,
          "latency_s": 1.637594,
          "model": "gpt-6-luna",
          "prompt_tokens": 1444,
          "reasoning_tokens": 49,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "友人が年賀状で宝くじが当たったと知らせてきて、昔の賭けに勝ったんだと思う。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9123242279747501,
      "jev_s": null,
      "judge_s": 0.9123242279747501,
      "luna_s": null,
      "total_s": 2.5504427020205185,
      "writer_s": 1.6381184740457684
    }
  },
  {
    "case_id": "U25-k01",
    "record": {
      "comment_id": "U25-k01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_correct"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 0.99
              },
              "A1b": {
                "qg": 0.96
              },
              "B": {
                "point_0": 0.97
              },
              "B2": {}
            },
            "input_tokens": 2717,
            "latency_s": 0.942009,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.0,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.98,
                "question": 0.02
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.99,
                  "hit": 0.98
                }
              },
              "B2": 0.02
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.98, 矛盾=0.02"
        },
        "jev": null,
        "luna": null
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
      "shadow_mismatch": null,
      "text": "新年の便りに盤面の次の手を書き添えて、二人は将棋を何十年も続けてたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9423237059963867,
      "jev_s": null,
      "judge_s": 0.9423237059963867,
      "luna_s": null,
      "total_s": 0.9423381650121883,
      "writer_s": 1.4459015801548958e-05
    }
  },
  {
    "case_id": "U25-k02",
    "record": {
      "comment_id": "U25-k02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_close"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 1.0
              },
              "B": {
                "point_0": 0.11
              }
            },
            "input_tokens": 1699,
            "latency_s": 0.753138,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.74,
                  "hit": 0.33
                }
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.33"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 103,
          "latency_s": 1.833182,
          "model": "gpt-6-luna",
          "prompt_tokens": 1444,
          "reasoning_tokens": 61,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！ほかの可能性も考えながら、推理を続けてみようか☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "離れて暮らす二人が、年始のはがきで一手ずつ棋譜をつなぐ対局だったんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.7534751020139083,
      "jev_s": null,
      "judge_s": 0.7534751020139083,
      "luna_s": null,
      "total_s": 2.592861347948201,
      "writer_s": 1.8393862459342927
    }
  },
  {
    "case_id": "U25-k03",
    "record": {
      "comment_id": "U25-k03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.88
              },
              "A2": {
                "kind": 0.77
              },
              "A3": {}
            },
            "input_tokens": 1883,
            "latency_s": 0.911152,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_multi": 0.04,
                "q_open": 0.85,
                "q_yesno": 0.11
              },
              "A3": 0.01,
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 90,
          "latency_s": 1.783344,
          "model": "gpt-6-luna",
          "prompt_tokens": 1436,
          "reasoning_tokens": 54,
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
      "shadow_mismatch": null,
      "text": "年賀状を通して二人は長く何かの勝負を続けていたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9114817118970677,
      "jev_s": null,
      "judge_s": 0.9114817118970677,
      "luna_s": null,
      "total_s": 2.695945252897218,
      "writer_s": 1.7844635410001501
    }
  },
  {
    "case_id": "U25-k04",
    "record": {
      "comment_id": "U25-k04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 0.99
              },
              "A1b": {
                "qg": 0.68
              },
              "A2": {
                "kind": 0.79
              },
              "A3": {}
            },
            "input_tokens": 1935,
            "latency_s": 0.920325,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.0,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.84,
                "question": 0.16
              },
              "A2": {
                "q_multi": 0.03,
                "q_open": 0.86,
                "q_yesno": 0.11
              },
              "A3": 0.01,
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 199,
          "latency_s": 2.722682,
          "model": "gpt-6-luna",
          "prompt_tokens": 1449,
          "reasoning_tokens": 159,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "二人は毎年顔を合わせて次の手を決めていたのかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "新年のはがきで将棋の続きを送り合ってたけど、二人は毎年顔を合わせて次の手を決めてたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9205579590052366,
      "jev_s": null,
      "judge_s": 0.9205579590052366,
      "luna_s": null,
      "total_s": 3.6436472280183807,
      "writer_s": 2.723089269013144
    }
  },
  {
    "case_id": "U25-k05",
    "record": {
      "comment_id": "U25-k05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_close"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "confidence": {
              "A1": {
                "major": 0.96
              },
              "A1b": {
                "qg": 0.94
              },
              "B": {
                "point_0": 0.97
              }
            },
            "input_tokens": 1693,
            "latency_s": 0.712474,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.97,
                "reaction": 0.02,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.97,
                "question": 0.03
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.98,
                  "hit": 0.0
                }
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 63,
          "latency_s": 1.543855,
          "model": "gpt-6-luna",
          "prompt_tokens": 1442,
          "reasoning_tokens": 30,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し推理を続けてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "年賀状には勝負の続きが記され、二人は毎年やりとりを重ねていたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.7128186819609255,
      "jev_s": null,
      "judge_s": 0.7128186819609255,
      "luna_s": null,
      "total_s": 2.2577894530259073,
      "writer_s": 1.5449707710649818
    }
  },
  {
    "case_id": "U25-k06",
    "record": {
      "comment_id": "U25-k06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_wrong"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 0.93
              },
              "A1b": {
                "qg": 1.0
              },
              "A2": {
                "kind": 0.83
              },
              "B": {
                "point_0": 1.0
              }
            },
            "guess_demoted": true,
            "input_tokens": 2009,
            "latency_s": 1.301577,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.01,
                "question_or_guess": 0.94,
                "reaction": 0.04,
                "request": 0.01
              },
              "A1b": {
                "guess": 1.0,
                "question": 0.0
              },
              "A2": {
                "q_multi": 0.03,
                "q_open": 0.89,
                "q_yesno": 0.08
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 77,
          "latency_s": 1.901042,
          "model": "gpt-6-luna",
          "prompt_tokens": 1441,
          "reasoning_tokens": 40,
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
      "shadow_mismatch": null,
      "text": "友人は年賀状で、55年ぶりに中学時代の話を思い出したと知らせたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.301847410039045,
      "jev_s": null,
      "judge_s": 1.301847410039045,
      "luna_s": null,
      "total_s": 3.2145397280110046,
      "writer_s": 1.9126923179719597
    }
  },
  {
    "case_id": "U25-t01",
    "record": {
      "comment_id": "U25-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": "年賀状将棋",
          "debug": {
            "calls": 1,
            "confidence": {
              "A1": {
                "major": 0.89
              }
            },
            "input_tokens": 779,
            "latency_s": 0.241061,
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.01,
                "question_or_guess": 0.91,
                "reaction": 0.06,
                "request": 0.02
              },
              "A_bare": 0.88
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.88"
        },
        "jev": null,
        "luna": null
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
      "shadow_mismatch": null,
      "text": "年賀状将棋？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.24118056101724505,
      "jev_s": null,
      "judge_s": 0.24118056101724505,
      "luna_s": null,
      "total_s": 3.5073284149402753,
      "writer_s": 3.26614785392303
    }
  },
  {
    "case_id": "U25-t02",
    "record": {
      "comment_id": "U25-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": "野球部",
          "debug": {
            "calls": 1,
            "confidence": {
              "A1": {
                "major": 0.7
              }
            },
            "input_tokens": 776,
            "latency_s": 0.249714,
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.01,
                "question_or_guess": 0.76,
                "reaction": 0.23,
                "request": 0.0
              },
              "A_bare": 1.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 1.00"
        },
        "jev": null,
        "luna": null
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
      "shadow_mismatch": null,
      "text": "野球部",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.24987437692470849,
      "jev_s": null,
      "judge_s": 0.24987437692470849,
      "luna_s": null,
      "total_s": 3.378967549884692,
      "writer_s": 3.1290931729599833
    }
  },
  {
    "case_id": "c-ask_howto-01",
    "record": {
      "comment_id": "c-ask_howto-01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "ask_howto"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A2": {
                "kind": 1.0
              }
            },
            "input_tokens": 1049,
            "latency_s": 0.483827,
            "major": "request",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.0,
                "request": 1.0
              },
              "A2": {
                "ask_hint": 0.0,
                "ask_howto": 1.0,
                "ask_spoiler": 0.0
              },
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "ask_howto",
          "reason": "段A=request→ask_howto"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 37,
          "latency_s": 2.081779,
          "model": "gpt-6-luna",
          "prompt_tokens": 1421,
          "reasoning_tokens": 0,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる質問をコメントしてね。探偵が答えるよ！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "これどうやって遊ぶの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.48400251602288336,
      "jev_s": null,
      "judge_s": 0.48400251602288336,
      "luna_s": null,
      "total_s": 2.5668596719624475,
      "writer_s": 2.082857155939564
    }
  },
  {
    "case_id": "c-greeting-05",
    "record": {
      "comment_id": "c-greeting-05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "greeting"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A2": {
                "kind": 0.99
              }
            },
            "input_tokens": 1150,
            "latency_s": 0.444694,
            "major": "reaction",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "greeting": 0.99,
                "impression": 0.01,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "greeting",
          "reason": "段A=reaction→greeting"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 23,
          "latency_s": 1.160543,
          "model": "gpt-6-luna",
          "prompt_tokens": 1416,
          "reasoning_tokens": 0,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "こんにちは！初コメントありがとう、これからよろしくね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "こんにちは、初コメです",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.444888170924969,
      "jev_s": null,
      "judge_s": 0.444888170924969,
      "luna_s": null,
      "total_s": 1.6061796299181879,
      "writer_s": 1.1612914589932188
    }
  },
  {
    "case_id": "c-request-04",
    "record": {
      "comment_id": "c-request-04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "request"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "confidence": {
              "A1": {
                "major": 0.54
              },
              "A2": {
                "kind": 0.93
              }
            },
            "input_tokens": 1156,
            "latency_s": 0.464916,
            "major": "reaction",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.02,
                "reaction": 0.63,
                "request": 0.35
              },
              "A2": {
                "chat": 0.01,
                "cheer": 0.01,
                "complaint": 0.01,
                "greeting": 0.0,
                "impression": 0.03,
                "mention": 0.0,
                "request": 0.94
              },
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "request",
          "reason": "段A=reaction→request"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 82,
          "latency_s": 2.88517,
          "model": "gpt-6-luna",
          "prompt_tokens": 1419,
          "reasoning_tokens": 54,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "リクエストありがとう、うれしいよ！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "短めの問題リクエストです",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.4650636789156124,
      "jev_s": null,
      "judge_s": 0.4650636789156124,
      "luna_s": null,
      "total_s": 3.3512683858862147,
      "writer_s": 2.8862047069706023
    }
  },
  {
    "case_id": "c-emoji_only-03",
    "record": {
      "comment_id": "c-emoji_only-03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "emoji_only"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 0,
            "confidence": {},
            "input_tokens": 0,
            "latency_s": 0.0,
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {},
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "emoji_only",
          "reason": "段0規則: emoji_only"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 59,
          "latency_s": 1.534639,
          "model": "gpt-6-luna",
          "prompt_tokens": 1413,
          "reasoning_tokens": 34,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "びっくりしたね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "😮",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 2.638192381709814e-05,
      "jev_s": null,
      "judge_s": 2.638192381709814e-05,
      "luna_s": null,
      "total_s": 1.5350637818919495,
      "writer_s": 1.5350373999681324
    }
  },
  {
    "case_id": "c-spam-02",
    "record": {
      "comment_id": "c-spam-02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "spam"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A2": {
                "kind": 1.0
              }
            },
            "input_tokens": 1093,
            "latency_s": 0.48622,
            "major": "inappropriate",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "spam",
          "reason": "段A=inappropriate→spam"
        },
        "jev": null,
        "luna": null
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
      "shadow_mismatch": null,
      "text": "フォローしてくれたら相互します！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.4863466590177268,
      "jev_s": null,
      "judge_s": 0.4863466590177268,
      "luna_s": null,
      "total_s": 0.4863507730187848,
      "writer_s": 4.114001058042049e-06
    }
  },
  {
    "case_id": "c-abuse-06",
    "record": {
      "comment_id": "c-abuse-06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "abuse"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "confidence": {
              "A1": {
                "major": 0.8
              },
              "A2": {
                "kind": 1.0
              }
            },
            "input_tokens": 1093,
            "latency_s": 0.481856,
            "major": "inappropriate",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.84,
                "other": 0.01,
                "question_or_guess": 0.01,
                "reaction": 0.14,
                "request": 0.0
              },
              "A2": {
                "abuse": 1.0,
                "personal_info": 0.0,
                "spam": 0.0,
                "troll": 0.0
              },
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "abuse",
          "reason": "段A=inappropriate→abuse"
        },
        "jev": null,
        "luna": null
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
      "shadow_mismatch": null,
      "text": "作者って絶対友達いないでしょ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.48202519200276583,
      "jev_s": null,
      "judge_s": 0.48202519200276583,
      "luna_s": null,
      "total_s": 0.48207137698773295,
      "writer_s": 4.618498496711254e-05
    }
  }
];
