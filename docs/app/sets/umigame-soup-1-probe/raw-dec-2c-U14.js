window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["dec-2c/U14"] = [
  {
    "case_id": "U14-e01",
    "record": {
      "comment_id": "U14-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "qg": 0.98
              },
              "A2": {
                "kind": 0.91
              },
              "B": {
                "point_0": 0.88,
                "point_1": 1.0
              },
              "C": {}
            },
            "input_tokens": 2733,
            "latency_s": 1.116075,
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
                "q_multi": 0.02,
                "q_open": 0.04,
                "q_yesno": 0.94
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.08,
                  "hit": 0.04
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.17
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 159,
          "latency_s": 2.840871,
          "model": "gpt-6-luna",
          "prompt_tokens": 1436,
          "reasoning_tokens": 123,
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
      "text": "主人はパンを作るときに、その卵を材料として使ってるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.1163128759944811,
      "jev_s": null,
      "judge_s": 1.1163128759944811,
      "luna_s": null,
      "total_s": 3.9784576640231535,
      "writer_s": 2.8621447880286723
    }
  },
  {
    "case_id": "U14-e02",
    "record": {
      "comment_id": "U14-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "qg": 0.98
              },
              "A2": {
                "kind": 1.0
              },
              "B": {
                "point_0": 1.0,
                "point_1": 1.0
              },
              "C": {},
              "D": {
                "answer": 1.0
              }
            },
            "input_tokens": 3399,
            "latency_s": 1.421866,
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
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.59,
              "D": {
                "irrelevant": 0.0,
                "no": 1.0,
                "yes": 0.0
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 69,
          "latency_s": 1.490357,
          "model": "gpt-6-luna",
          "prompt_tokens": 1429,
          "reasoning_tokens": 42,
          "slot": "判定語 + 一言"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。次の質問もどうぞ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "ここでいう卵は鶏の卵ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.422170690027997,
      "jev_s": null,
      "judge_s": 1.422170690027997,
      "luna_s": null,
      "total_s": 2.9135962560540065,
      "writer_s": 1.4914255660260096
    }
  },
  {
    "case_id": "U14-e03",
    "record": {
      "comment_id": "U14-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "qg": 0.98
              },
              "A2": {
                "kind": 1.0
              },
              "B": {
                "point_0": 0.93,
                "point_1": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.99
              }
            },
            "input_tokens": 3441,
            "latency_s": 1.323408,
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
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.05,
                  "hit": 0.03
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.56,
              "D": {
                "irrelevant": 0.0,
                "no": 0.99,
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 83,
          "latency_s": 1.701078,
          "model": "gpt-6-luna",
          "prompt_tokens": 1436,
          "reasoning_tokens": 53,
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
      "text": "卵は店の中で飼っている鶏が産んだものですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.3237872020108625,
      "jev_s": null,
      "judge_s": 1.3237872020108625,
      "luna_s": null,
      "total_s": 3.0255349919898435,
      "writer_s": 1.701747789978981
    }
  },
  {
    "case_id": "U14-e04",
    "record": {
      "comment_id": "U14-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "qg": 0.02
              },
              "A2": {
                "kind": 0.99
              },
              "B": {
                "point_0": 1.0,
                "point_1": 1.0
              },
              "C": {}
            },
            "input_tokens": 2723,
            "latency_s": 1.133676,
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
                "guess": 0.49,
                "question": 0.51
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
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.18
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 166,
          "latency_s": 3.436859,
          "model": "gpt-6-luna",
          "prompt_tokens": 1434,
          "reasoning_tokens": 129,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で、聞いてみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "卵を大切にしているのは、割れやすいからですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.1339509789831936,
      "jev_s": null,
      "judge_s": 1.1339509789831936,
      "luna_s": null,
      "total_s": 4.571905531920493,
      "writer_s": 3.437954552937299
    }
  },
  {
    "case_id": "U14-e05",
    "record": {
      "comment_id": "U14-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "point_0": 0.89,
                "point_1": 0.99
              },
              "C": {},
              "D": {
                "answer": 0.45
              }
            },
            "input_tokens": 3441,
            "latency_s": 1.370627,
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
                  "close": 0.07,
                  "hit": 0.03
                },
                "point_1": {
                  "close": 0.01,
                  "hit": 0.0
                }
              },
              "C": 0.54,
              "D": {
                "irrelevant": 0.01,
                "no": 0.36,
                "yes": 0.63
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 91,
          "latency_s": 1.759631,
          "model": "gpt-6-luna",
          "prompt_tokens": 1436,
          "reasoning_tokens": 67,
          "slot": "判定語 + 一言"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "主人は卵をゆでたり割ったりしたことが一度もないんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.3709405229892582,
      "jev_s": null,
      "judge_s": 1.3709405229892582,
      "luna_s": null,
      "total_s": 3.1309558269567788,
      "writer_s": 1.7600153039675206
    }
  },
  {
    "case_id": "U14-e06",
    "record": {
      "comment_id": "U14-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
      "final": {
        "answer": "irrelevant",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 0.99
              },
              "A1b": {
                "qg": 0.96
              },
              "A2": {
                "kind": 0.99
              },
              "B": {
                "point_0": 1.0,
                "point_1": 0.99
              },
              "C": {},
              "D": {
                "answer": 0.24
              }
            },
            "input_tokens": 3405,
            "latency_s": 1.379638,
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
                "guess": 0.02,
                "question": 0.98
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
                },
                "point_1": {
                  "close": 0.01,
                  "hit": 0.0
                }
              },
              "C": 0.62,
              "D": {
                "irrelevant": 0.05,
                "no": 0.46,
                "yes": 0.49
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 88,
          "latency_s": 2.009723,
          "model": "gpt-6-luna",
          "prompt_tokens": 1430,
          "reasoning_tokens": 55,
          "slot": "判定語 + 一言"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "パンの生地に卵を混ぜる工程はありますか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.3800797750009224,
      "jev_s": null,
      "judge_s": 1.3800797750009224,
      "luna_s": null,
      "total_s": 3.390254645026289,
      "writer_s": 2.0101748700253665
    }
  },
  {
    "case_id": "U14-e07",
    "record": {
      "comment_id": "U14-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "qg": 0.96
              },
              "A2": {
                "kind": 0.97
              },
              "B": {
                "point_0": 1.0,
                "point_1": 1.0
              },
              "C": {}
            },
            "input_tokens": 2713,
            "latency_s": 1.18965,
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
                "guess": 0.02,
                "question": 0.98
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
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.18
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 266,
          "latency_s": 4.244839,
          "model": "gpt-6-luna",
          "prompt_tokens": 1432,
          "reasoning_tokens": 214,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "「卵は商品名に関係している？」のように、はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "卵は商品名や店の名前に関係しているんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.1901295280549675,
      "jev_s": null,
      "judge_s": 1.1901295280549675,
      "luna_s": null,
      "total_s": 5.435724868089892,
      "writer_s": 4.2455953400349244
    }
  },
  {
    "case_id": "U14-e08",
    "record": {
      "comment_id": "U14-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "point_0": 1.0,
                "point_1": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.42
              }
            },
            "input_tokens": 3417,
            "latency_s": 1.375071,
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
                "q_open": 0.0,
                "q_yesno": 0.99
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.44,
              "D": {
                "irrelevant": 0.03,
                "no": 0.36,
                "yes": 0.61
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 34,
          "latency_s": 1.3177,
          "model": "gpt-6-luna",
          "prompt_tokens": 1430,
          "reasoning_tokens": 15,
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
      "text": "お客さんも卵のおかげだと知ってるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.375384475919418,
      "jev_s": null,
      "judge_s": 1.375384475919418,
      "luna_s": null,
      "total_s": 2.6935701959300786,
      "writer_s": 1.3181857200106606
    }
  },
  {
    "case_id": "U14-e09",
    "record": {
      "comment_id": "U14-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "qg": 0.98
              },
              "A2": {
                "kind": 1.0
              },
              "B": {
                "point_0": 1.0,
                "point_1": 1.0
              },
              "C": {}
            },
            "input_tokens": 2723,
            "latency_s": 1.896427,
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
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.12
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 214,
          "latency_s": 3.44711,
          "model": "gpt-6-luna",
          "prompt_tokens": 1434,
          "reasoning_tokens": 176,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞いてみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "卵はパン屋の主人が自分で買いに行くんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.8967191849369556,
      "jev_s": null,
      "judge_s": 1.8967191849369556,
      "luna_s": null,
      "total_s": 5.344915791996755,
      "writer_s": 3.448196607059799
    }
  },
  {
    "case_id": "U14-e10",
    "record": {
      "comment_id": "U14-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
      "final": {
        "answer": "irrelevant",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "irrelevant",
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
                "kind": 1.0
              },
              "B": {
                "point_0": 1.0,
                "point_1": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.51
              }
            },
            "input_tokens": 3387,
            "latency_s": 1.396467,
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
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.51,
              "D": {
                "irrelevant": 0.67,
                "no": 0.15,
                "yes": 0.18
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 81,
          "latency_s": 1.729148,
          "model": "gpt-6-luna",
          "prompt_tokens": 1428,
          "reasoning_tokens": 48,
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
      "shadow_mismatch": null,
      "text": "お店のオーブンは電気式ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.3969889259897172,
      "jev_s": null,
      "judge_s": 1.3969889259897172,
      "luna_s": null,
      "total_s": 3.1271206830861047,
      "writer_s": 1.7301317570963874
    }
  },
  {
    "case_id": "U14-e11",
    "record": {
      "comment_id": "U14-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "qg": 1.0
              },
              "A2": {
                "kind": 0.53
              },
              "A3": {}
            },
            "input_tokens": 1877,
            "latency_s": 0.898757,
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
                "q_multi": 0.21,
                "q_open": 0.1,
                "q_yesno": 0.69
              },
              "A3": 0.57,
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.57"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 160,
          "latency_s": 2.844489,
          "model": "gpt-6-luna",
          "prompt_tokens": 1436,
          "reasoning_tokens": 109,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞いてごらん。たとえば「卵は食べ物なの？」だよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "卵は本物の食べ物なの？それとも卵の形をした何か？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.8990143190603703,
      "jev_s": null,
      "judge_s": 0.8990143190603703,
      "luna_s": null,
      "total_s": 3.7555227030534297,
      "writer_s": 2.8565083839930594
    }
  },
  {
    "case_id": "U14-e12",
    "record": {
      "comment_id": "U14-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "qg": 1.0
              },
              "A2": {
                "kind": 0.99
              }
            },
            "input_tokens": 1514,
            "latency_s": 0.677836,
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
                "guess": 0.0,
                "question": 1.0
              },
              "A2": {
                "q_multi": 0.99,
                "q_open": 0.0,
                "q_yesno": 0.01
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 113,
          "latency_s": 2.221817,
          "model": "gpt-6-luna",
          "prompt_tokens": 1438,
          "reasoning_tokens": 75,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。まずはどっちから聞こうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "パンに卵を使ってるの？その卵を割るのは主人以外の人？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.678039675927721,
      "jev_s": null,
      "judge_s": 0.678039675927721,
      "luna_s": null,
      "total_s": 2.9008439669851214,
      "writer_s": 2.2228042910574004
    }
  },
  {
    "case_id": "U14-e13",
    "record": {
      "comment_id": "U14-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "major": 0.93
              },
              "A1b": {
                "qg": 0.96
              },
              "A2": {
                "kind": 0.99
              },
              "A3": {}
            },
            "input_tokens": 1865,
            "latency_s": 0.973364,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.94,
                "reaction": 0.04,
                "request": 0.02
              },
              "A1b": {
                "guess": 0.02,
                "question": 0.98
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.99,
                "q_yesno": 0.01
              },
              "A3": 0.02,
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.02"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 81,
          "latency_s": 2.160258,
          "model": "gpt-6-luna",
          "prompt_tokens": 1433,
          "reasoning_tokens": 45,
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
      "text": "卵を使わずに、どうしてパンがおいしくなるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9737390270456672,
      "jev_s": null,
      "judge_s": 0.9737390270456672,
      "luna_s": null,
      "total_s": 3.1345641099615023,
      "writer_s": 2.160825082915835
    }
  },
  {
    "case_id": "U14-e14",
    "record": {
      "comment_id": "U14-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "qg": 0.96
              },
              "A2": {
                "kind": 0.99
              },
              "A3": {}
            },
            "input_tokens": 1861,
            "latency_s": 1.030983,
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
                "guess": 0.02,
                "question": 0.98
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.99,
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 149,
          "latency_s": 3.094399,
          "model": "gpt-6-luna",
          "prompt_tokens": 1432,
          "reasoning_tokens": 104,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞いてごらん。卵が何か、かな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "主人が大切にしている卵って、何の卵なんでしょう？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.0312275410396978,
      "jev_s": null,
      "judge_s": 1.0312275410396978,
      "luna_s": null,
      "total_s": 4.127062856103294,
      "writer_s": 3.0958353150635958
    }
  },
  {
    "case_id": "U14-e15",
    "record": {
      "comment_id": "U14-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "qg": 0.86
              },
              "A2": {
                "kind": 0.99
              },
              "A3": {}
            },
            "input_tokens": 1857,
            "latency_s": 1.098206,
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
                "q_multi": 0.0,
                "q_open": 0.99,
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 138,
          "latency_s": 3.07924,
          "model": "gpt-6-luna",
          "prompt_tokens": 1431,
          "reasoning_tokens": 102,
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
      "text": "どうやって卵がパンのおいしさにつながっているの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.098462122026831,
      "jev_s": null,
      "judge_s": 1.098462122026831,
      "luna_s": null,
      "total_s": 4.1785142589360476,
      "writer_s": 3.0800521369092166
    }
  },
  {
    "case_id": "U14-e16",
    "record": {
      "comment_id": "U14-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "qg": 0.9
              },
              "B": {
                "point_0": 0.99,
                "point_1": 0.93
              },
              "B2": {}
            },
            "input_tokens": 2999,
            "latency_s": 1.042028,
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
                "guess": 0.95,
                "question": 0.05
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.99,
                  "hit": 0.99
                },
                "point_1": {
                  "close": 0.97,
                  "hit": 0.95
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
          "reason": "段A=guess→guess_correct, 要点最低=0.95, 矛盾=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！「卵」はパン職人の卵、つまり見習いのこと。主人が一人前に育てたその職人が、いまおいしいパンを焼いている。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "卵ってパン職人の見習いだったってこと？その人が育ってパンを焼いてるから、おいしいのはこの卵のおかげなんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.0422760361107066,
      "jev_s": null,
      "judge_s": 1.0422760361107066,
      "luna_s": null,
      "total_s": 1.0422901911661029,
      "writer_s": 1.4155055396258831e-05
    }
  },
  {
    "case_id": "U14-e17",
    "record": {
      "comment_id": "U14-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "qg": 1.0
              },
              "B": {
                "point_0": 1.0,
                "point_1": 0.89
              },
              "B2": {}
            },
            "input_tokens": 3031,
            "latency_s": 0.91201,
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
                "guess": 1.0,
                "question": 0.0
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 1.0,
                  "hit": 1.0
                },
                "point_1": {
                  "close": 0.9600000000000001,
                  "hit": 0.93
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
          "reason": "段A=guess→guess_correct, 要点最低=0.93, 矛盾=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！「卵」はパン職人の卵、つまり見習いのこと。主人が一人前に育てたその職人が、いまおいしいパンを焼いている。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "食べ物の卵じゃなくて、パン職人の見習いをそう呼んでたんだね。今はその人が焼いているから、主人が自慢するのも分かる。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9122787050437182,
      "jev_s": null,
      "judge_s": 0.9122787050437182,
      "luna_s": null,
      "total_s": 0.9122832320863381,
      "writer_s": 4.527042619884014e-06
    }
  },
  {
    "case_id": "U14-e18",
    "record": {
      "comment_id": "U14-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "qg": 0.9
              },
              "B": {
                "point_0": 0.88,
                "point_1": 0.99
              }
            },
            "input_tokens": 2038,
            "latency_s": 0.738563,
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
                "guess": 0.95,
                "question": 0.05
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.98,
                  "hit": 0.92
                },
                "point_1": {
                  "close": 0.01,
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 86,
          "latency_s": 1.882642,
          "model": "gpt-6-luna",
          "prompt_tokens": 1431,
          "reasoning_tokens": 51,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！質問しながら、もう少し考えてみようか☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "卵はパン屋で修業中の人のことなんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.7388170490739867,
      "jev_s": null,
      "judge_s": 0.7388170490739867,
      "luna_s": null,
      "total_s": 2.6280199731700122,
      "writer_s": 1.8892029240960255
    }
  },
  {
    "case_id": "U14-e19",
    "record": {
      "comment_id": "U14-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.96
              },
              "B": {
                "point_0": 0.99,
                "point_1": 0.79
              },
              "B2": {}
            },
            "input_tokens": 3023,
            "latency_s": 0.91253,
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
                "guess": 0.98,
                "question": 0.02
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 1.0,
                  "hit": 0.99
                },
                "point_1": {
                  "close": 0.89,
                  "hit": 0.86
                }
              },
              "B2": 0.98
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.86, 矛盾=0.98"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 91,
          "latency_s": 1.931705,
          "model": "gpt-6-luna",
          "prompt_tokens": 1460,
          "reasoning_tokens": 61,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し考えてみようか 🧐"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "卵はパン職人の見習いで、その人が焼くパンがおいしいんだね。でも主人はパン作りを教えてなくて、その人が勝手に覚えたのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9128139590611681,
      "jev_s": null,
      "judge_s": 0.9128139590611681,
      "luna_s": null,
      "total_s": 2.8450124820228666,
      "writer_s": 1.9321985229616985
    }
  },
  {
    "case_id": "U14-e20",
    "record": {
      "comment_id": "U14-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "major": 1.0
              },
              "A1b": {
                "qg": 0.96
              },
              "A2": {
                "kind": 0.49
              },
              "B": {
                "point_0": 1.0,
                "point_1": 1.0
              }
            },
            "guess_demoted": true,
            "input_tokens": 2440,
            "latency_s": 0.867524,
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
                "guess": 0.98,
                "question": 0.02
              },
              "A2": {
                "q_multi": 0.08,
                "q_open": 0.66,
                "q_yesno": 0.26
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                },
                "point_1": {
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 72,
          "latency_s": 1.743522,
          "model": "gpt-6-luna",
          "prompt_tokens": 1455,
          "reasoning_tokens": 35,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "卵を産む鶏を店の奥で大事に飼っていて、その鶏の餌がパン生地に混ざってるんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.8678353739669546,
      "jev_s": null,
      "judge_s": 0.8678353739669546,
      "luna_s": null,
      "total_s": 2.6127862610155717,
      "writer_s": 1.744950887048617
    }
  },
  {
    "case_id": "U14-e21",
    "record": {
      "comment_id": "U14-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "major": 1.0
              },
              "A1b": {
                "qg": 0.98
              },
              "A2": {
                "kind": 0.8
              },
              "B": {
                "point_0": 1.0,
                "point_1": 0.97
              }
            },
            "guess_demoted": true,
            "input_tokens": 2384,
            "latency_s": 0.906828,
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
                "guess": 0.99,
                "question": 0.01
              },
              "A2": {
                "q_multi": 0.02,
                "q_open": 0.87,
                "q_yesno": 0.11
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                },
                "point_1": {
                  "close": 0.02,
                  "hit": 0.01
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 88,
          "latency_s": 1.737829,
          "model": "gpt-6-luna",
          "prompt_tokens": 1441,
          "reasoning_tokens": 51,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "卵はパン屋の幸運のお守りで、主人がそう思い込んでるだけだと思う。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9071211350383237,
      "jev_s": null,
      "judge_s": 0.9071211350383237,
      "luna_s": null,
      "total_s": 2.651492514065467,
      "writer_s": 1.7443713790271431
    }
  },
  {
    "case_id": "U14-k01",
    "record": {
      "comment_id": "U14-k01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "qg": 0.92
              },
              "B": {
                "point_0": 0.91,
                "point_1": 0.96
              }
            },
            "input_tokens": 2089,
            "latency_s": 0.662566,
            "major": "guess",
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
                "guess": 0.96,
                "question": 0.04
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.06,
                  "hit": 0.04
                },
                "point_1": {
                  "close": 0.99,
                  "hit": 0.97
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
          "reason": "段A=guess→guess_close, 要点最低=0.04"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 79,
          "latency_s": 2.380556,
          "model": "gpt-6-luna",
          "prompt_tokens": 1448,
          "reasoning_tokens": 46,
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
      "text": "店が育てた職人見習いが今は焼き手で、その腕前がパンのおいしさにつながってるんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.6627007509814575,
      "jev_s": null,
      "judge_s": 0.6627007509814575,
      "luna_s": null,
      "total_s": 3.043764414032921,
      "writer_s": 2.3810636630514637
    }
  },
  {
    "case_id": "U14-k02",
    "record": {
      "comment_id": "U14-k02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "major": 0.9
              },
              "A1b": {
                "qg": 0.98
              },
              "B": {
                "point_0": 0.46,
                "point_1": 0.97
              }
            },
            "input_tokens": 2098,
            "latency_s": 0.614131,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.92,
                "reaction": 0.07,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.99,
                "question": 0.01
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.36,
                  "hit": 0.36
                },
                "point_1": {
                  "close": 0.99,
                  "hit": 0.98
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
          "reason": "段A=guess→guess_close, 要点最低=0.36"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 97,
          "latency_s": 1.869425,
          "model": "gpt-6-luna",
          "prompt_tokens": 1451,
          "reasoning_tokens": 67,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！推理を続けてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "パン職人を目指して店で修業する若手を主人が大切にし、今ではその人が店のパンを焼いてるんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.614254018990323,
      "jev_s": null,
      "judge_s": 0.614254018990323,
      "luna_s": null,
      "total_s": 2.4848906310508028,
      "writer_s": 1.8706366120604798
    }
  },
  {
    "case_id": "U14-k03",
    "record": {
      "comment_id": "U14-k03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "major": 0.96
              },
              "A1b": {
                "qg": 0.64
              },
              "A2": {
                "kind": 0.58
              },
              "A3": {}
            },
            "input_tokens": 1917,
            "latency_s": 0.937392,
            "major": "question",
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
                "guess": 0.82,
                "question": 0.18
              },
              "A2": {
                "q_multi": 0.06,
                "q_open": 0.72,
                "q_yesno": 0.22
              },
              "A3": 0.05,
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.05"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 106,
          "latency_s": 2.323687,
          "model": "gpt-6-luna",
          "prompt_tokens": 1446,
          "reasoning_tokens": 70,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形にして、聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "卵は修業中の職人を指す呼び名だけど、今は仕込みを手伝う段階なんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9376379089662805,
      "jev_s": null,
      "judge_s": 0.9376379089662805,
      "luna_s": null,
      "total_s": 3.262636773986742,
      "writer_s": 2.3249988650204614
    }
  },
  {
    "case_id": "U14-k04",
    "record": {
      "comment_id": "U14-k04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "major": 0.95
              },
              "A1b": {
                "qg": 0.96
              },
              "B": {
                "point_0": 0.91,
                "point_1": 0.88
              }
            },
            "input_tokens": 2083,
            "latency_s": 0.689431,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.01,
                "question_or_guess": 0.96,
                "reaction": 0.02,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.98,
                "question": 0.02
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.97,
                  "hit": 0.94
                },
                "point_1": {
                  "close": 0.9500000000000001,
                  "hit": 0.03
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
          "reason": "段A=guess→guess_close, 要点最低=0.03"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 76,
          "latency_s": 1.768958,
          "model": "gpt-6-luna",
          "prompt_tokens": 1446,
          "reasoning_tokens": 43,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し推理を続けてみようか😉"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "卵はパン職人の見習いだけど、店では生地をこねる作業までを担当しているんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.6896958119468763,
      "jev_s": null,
      "judge_s": 0.6896958119468763,
      "luna_s": null,
      "total_s": 2.4597357630264014,
      "writer_s": 1.770039951079525
    }
  },
  {
    "case_id": "U14-k05",
    "record": {
      "comment_id": "U14-k05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "qg": 0.96
              },
              "B": {
                "point_0": 0.94,
                "point_1": 0.99
              }
            },
            "input_tokens": 2062,
            "latency_s": 0.732934,
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
                "guess": 0.98,
                "question": 0.02
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.98,
                  "hit": 0.02
                },
                "point_1": {
                  "close": 0.01,
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 73,
          "latency_s": 1.960209,
          "model": "gpt-6-luna",
          "prompt_tokens": 1439,
          "reasoning_tokens": 44,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し考えてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "卵は食べ物じゃなく、店で働く人のことをそう呼んでいたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.7332324370509014,
      "jev_s": null,
      "judge_s": 0.7332324370509014,
      "luna_s": null,
      "total_s": 2.6941318650497124,
      "writer_s": 1.960899427998811
    }
  },
  {
    "case_id": "U14-k06",
    "record": {
      "comment_id": "U14-k06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
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
                "qg": 1.0
              },
              "A2": {
                "kind": 0.76
              },
              "B": {
                "point_0": 0.94,
                "point_1": 1.0
              }
            },
            "guess_demoted": true,
            "input_tokens": 2400,
            "latency_s": 0.89122,
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
                "guess": 1.0,
                "question": 0.0
              },
              "A2": {
                "q_multi": 0.05,
                "q_open": 0.84,
                "q_yesno": 0.11
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.04,
                  "hit": 0.02
                },
                "point_1": {
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 79,
          "latency_s": 1.522344,
          "model": "gpt-6-luna",
          "prompt_tokens": 1445,
          "reasoning_tokens": 42,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "主人の大事な卵は常連客から贈られた飾りで、棚に置いてあるだけなんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.891596143017523,
      "jev_s": null,
      "judge_s": 0.891596143017523,
      "luna_s": null,
      "total_s": 2.414661200949922,
      "writer_s": 1.5230650579323992
    }
  },
  {
    "case_id": "U14-t01",
    "record": {
      "comment_id": "U14-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "c764429cc6b6",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": "パン職人の卵",
          "debug": {
            "calls": 1,
            "confidence": {
              "A1": {
                "major": 0.99
              }
            },
            "input_tokens": 780,
            "latency_s": 0.264689,
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
              "A_bare": 0.86
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.86"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "何がパン職人の卵なのか教えてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "パン職人の卵？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.2648170730099082,
      "jev_s": null,
      "judge_s": 0.2648170730099082,
      "luna_s": null,
      "total_s": 3.3759099011076614,
      "writer_s": 3.1110928280977532
    }
  },
  {
    "case_id": "U14-t02",
    "record": {
      "comment_id": "U14-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "c764429cc6b6",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": "いちごジャム",
          "debug": {
            "calls": 1,
            "confidence": {
              "A1": {
                "major": 0.85
              }
            },
            "input_tokens": 778,
            "latency_s": 0.218992,
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.01,
                "question_or_guess": 0.88,
                "reaction": 0.1,
                "request": 0.01
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
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "いちごジャムがどうしたのか聞かせてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "いちごジャム",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.219122439972125,
      "jev_s": null,
      "judge_s": 0.219122439972125,
      "luna_s": null,
      "total_s": 4.017288203001954,
      "writer_s": 3.7981657630298287
    }
  },
  {
    "case_id": "c-ask_hint-04",
    "record": {
      "comment_id": "c-ask_hint-04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "ask_hint"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "confidence": {
              "A1": {
                "major": 0.46
              },
              "A2": {
                "kind": 0.94
              }
            },
            "input_tokens": 1051,
            "latency_s": 0.532912,
            "major": "request",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.11,
                "reaction": 0.32,
                "request": 0.57
              },
              "A2": {
                "ask_hint": 0.96,
                "ask_howto": 0.02,
                "ask_spoiler": 0.02
              },
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "ask_hint",
          "reason": "段A=request→ask_hint"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 89,
          "latency_s": 1.848422,
          "model": "gpt-6-luna",
          "prompt_tokens": 1423,
          "reasoning_tokens": 50,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ヒントは出せないけど、質問で少しずつ絞っていこうね！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "詰まった、助けて🙏",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.533043508999981,
      "jev_s": null,
      "judge_s": 0.533043508999981,
      "luna_s": null,
      "total_s": 2.3822756320005283,
      "writer_s": 1.8492321230005473
    }
  },
  {
    "case_id": "c-impression-03",
    "record": {
      "comment_id": "c-impression-03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "impression"
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
                "kind": 0.98
              }
            },
            "input_tokens": 1158,
            "latency_s": 0.491376,
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
                "cheer": 0.01,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.98,
                "mention": 0.0,
                "request": 0.01
              },
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "impression",
          "reason": "段A=reaction→impression"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 105,
          "latency_s": 2.665619,
          "model": "gpt-6-luna",
          "prompt_tokens": 1423,
          "reasoning_tokens": 78,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "感想ありがとう、うれしいよ☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "今回の設定ちょっと怖くて好き",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.4914506709901616,
      "jev_s": null,
      "judge_s": 0.4914506709901616,
      "luna_s": null,
      "total_s": 3.1578218570211902,
      "writer_s": 2.6663711860310286
    }
  },
  {
    "case_id": "c-chat-02",
    "record": {
      "comment_id": "c-chat-02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "chat"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "confidence": {
              "A1": {
                "major": 0.99
              },
              "A2": {
                "kind": 0.64
              }
            },
            "input_tokens": 1152,
            "latency_s": 0.462623,
            "major": "reaction",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.01,
                "reaction": 0.99,
                "request": 0.0
              },
              "A2": {
                "chat": 0.69,
                "cheer": 0.1,
                "complaint": 0.01,
                "greeting": 0.02,
                "impression": 0.16,
                "mention": 0.01,
                "request": 0.01
              },
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "chat",
          "reason": "段A=reaction→chat"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 96,
          "latency_s": 1.6494,
          "model": "gpt-6-luna",
          "prompt_tokens": 1420,
          "reasoning_tokens": 61,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "通勤中に見てくれてありがとう！気をつけてね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "通勤中に見てます",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.4627701039426029,
      "jev_s": null,
      "judge_s": 0.4627701039426029,
      "luna_s": null,
      "total_s": 2.113195546902716,
      "writer_s": 1.6504254429601133
    }
  },
  {
    "case_id": "c-mention-01",
    "record": {
      "comment_id": "c-mention-01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "mention"
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
                "kind": 0.98
              }
            },
            "input_tokens": 1158,
            "latency_s": 0.493514,
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
                "complaint": 0.01,
                "greeting": 0.0,
                "impression": 0.01,
                "mention": 0.98,
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
          "kind": "mention",
          "reason": "段A=reaction→mention"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 57,
          "latency_s": 1.568108,
          "model": "gpt-6-luna",
          "prompt_tokens": 1423,
          "reasoning_tokens": 32,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "もちろん、一緒に考えよう！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "@mika これ一緒に解こ！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.4936509740073234,
      "jev_s": null,
      "judge_s": 0.4936509740073234,
      "luna_s": null,
      "total_s": 2.062613061047159,
      "writer_s": 1.5689620870398358
    }
  },
  {
    "case_id": "c-troll-05",
    "record": {
      "comment_id": "c-troll-05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "troll"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "confidence": {
              "A1": {
                "major": 0.94
              },
              "A2": {
                "kind": 1.0
              }
            },
            "input_tokens": 1085,
            "latency_s": 0.474725,
            "major": "inappropriate",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.95,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.05,
                "request": 0.0
              },
              "A2": {
                "abuse": 0.0,
                "personal_info": 0.0,
                "spam": 0.0,
                "troll": 1.0
              },
              "A_bare": 0.9
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "troll",
          "reason": "段A=inappropriate→troll"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U14",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "質問なら、はい・いいえで答えるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "無無無無むむむ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.4748895129887387,
      "jev_s": null,
      "judge_s": 0.4748895129887387,
      "luna_s": null,
      "total_s": 0.4748946470208466,
      "writer_s": 5.134032107889652e-06
    }
  },
  {
    "case_id": "c-personal_info-04",
    "record": {
      "comment_id": "c-personal_info-04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "005-bakers-egg",
      "errors": [],
      "fact_sheet_hash": "c764429cc6b6",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "personal_info"
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
            "input_tokens": 1109,
            "latency_s": 0.471322,
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
                "personal_info": 1.0,
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
          "kind": "personal_info",
          "reason": "段A=inappropriate→personal_info"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U14",
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
      "text": "本名はサンプル太郎、電話は090-0000-0456です",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.47145744506269693,
      "jev_s": null,
      "judge_s": 0.47145744506269693,
      "luna_s": null,
      "total_s": 0.47146118502132595,
      "writer_s": 3.739958629012108e-06
    }
  }
];
