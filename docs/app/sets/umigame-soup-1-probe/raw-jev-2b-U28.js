window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["jev-2b/U28"] = [
  {
    "case_id": "U28-e01",
    "record": {
      "comment_id": "U28-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "yes",
        "decision": "jev",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 5015,
            "latency_s": 1.203805,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
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
                "point_0": {
                  "close": 0.16,
                  "hit": 0.08
                },
                "point_1": {
                  "close": 0.03,
                  "hit": 0.01
                }
              },
              "C": 0.59,
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
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい！じっくり考えてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は以前にもウミガメのスープを飲んだことがありますか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.2042431060690433,
      "judge_s": 1.2042431060690433,
      "luna_s": null,
      "total_s": 1.20424993801862,
      "writer_s": 6.8319495767354965e-06
    }
  },
  {
    "case_id": "U28-e02",
    "record": {
      "comment_id": "U28-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "no",
        "decision": "jev",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "guess_demoted": true,
            "input_tokens": 5015,
            "latency_s": 1.249589,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
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
                "point_0": {
                  "close": 0.19,
                  "hit": 0.09
                },
                "point_1": {
                  "close": 0.05,
                  "hit": 0.02
                }
              },
              "C": 0.77,
              "D": {
                "irrelevant": 0.0,
                "no": 0.9,
                "yes": 0.1
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "いいえ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男が泣いたのは、スープの味に覚えがあったからですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.2500391179928556,
      "judge_s": 1.2500391179928556,
      "luna_s": null,
      "total_s": 1.2500446339836344,
      "writer_s": 5.515990778803825e-06
    }
  },
  {
    "case_id": "U28-e03",
    "record": {
      "comment_id": "U28-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "yes",
        "decision": "jev",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4961,
            "latency_s": 1.261003,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.83,
                "question": 0.17
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.16,
                  "hit": 0.1
                },
                "point_1": {
                  "close": 0.02,
                  "hit": 0.01
                }
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
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい！ひとつずつ確かめていこうね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は昔、遭難した経験があるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.2613776969956234,
      "judge_s": 1.2613776969956234,
      "luna_s": null,
      "total_s": 1.2613840260310099,
      "writer_s": 6.329035386443138e-06
    }
  },
  {
    "case_id": "U28-e04",
    "record": {
      "comment_id": "U28-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "yes",
        "decision": "jev",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "guess_demoted": true,
            "input_tokens": 5039,
            "latency_s": 1.146594,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
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
                "point_0": {
                  "close": 0.19,
                  "hit": 0.1
                },
                "point_1": {
                  "close": 0.12,
                  "hit": 0.06
                }
              },
              "C": 0.66,
              "D": {
                "irrelevant": 0.0,
                "no": 0.07,
                "yes": 0.93
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.06"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい！さあ、次はなにを聞く？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "本物だと聞いたことで、男の過去の記憶がよみがえったんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.14697503100615,
      "judge_s": 1.14697503100615,
      "luna_s": null,
      "total_s": 1.1523931649280712,
      "writer_s": 0.005418133921921253
    }
  },
  {
    "case_id": "U28-e05",
    "record": {
      "comment_id": "U28-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "no",
        "decision": "jev",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 5021,
            "latency_s": 1.223031,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.09,
                "question": 0.91
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.11,
                  "hit": 0.06
                },
                "point_1": {
                  "close": 0.1,
                  "hit": 0.05
                }
              },
              "C": 0.53,
              "D": {
                "irrelevant": 0.14,
                "no": 0.6,
                "yes": 0.26
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.05"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "いいえ。まだまだ聞いていいんだよ😌"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "スープを飲む前から、男は本物かどうか疑っていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.2234210830647498,
      "judge_s": 1.2234210830647498,
      "luna_s": null,
      "total_s": 1.223441017093137,
      "writer_s": 1.9934028387069702e-05
    }
  },
  {
    "case_id": "U28-e06",
    "record": {
      "comment_id": "U28-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 5,
            "input_tokens": 3728,
            "latency_s": 0.960968,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 253,
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
                  "close": 0.0,
                  "hit": 0.0
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.16
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 要点最低=0.00"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "形を変えて、はい・いいえで聞いてみようか😉"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "そのレストランは海辺にありますか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.9612945959670469,
      "judge_s": 0.9612945959670469,
      "luna_s": null,
      "total_s": 0.9613030779873952,
      "writer_s": 8.48202034831047e-06
    }
  },
  {
    "case_id": "U28-e07",
    "record": {
      "comment_id": "U28-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "no",
        "decision": "jev",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4967,
            "latency_s": 1.154392,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.14,
                "question": 0.86
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
                  "hit": 0.02
                },
                "point_1": {
                  "close": 0.16,
                  "hit": 0.09
                }
              },
              "C": 0.58,
              "D": {
                "irrelevant": 0.13,
                "no": 0.87,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "いいえ。まだまだ聞いていいんだよ😌"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "シェフは男のことを知っていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.1548380859894678,
      "judge_s": 1.1548380859894678,
      "luna_s": null,
      "total_s": 1.154844289063476,
      "writer_s": 6.203074008226395e-06
    }
  },
  {
    "case_id": "U28-e08",
    "record": {
      "comment_id": "U28-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "yes",
        "decision": "jev",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 5015,
            "latency_s": 1.175899,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
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
                "point_0": {
                  "close": 0.27,
                  "hit": 0.18
                },
                "point_1": {
                  "close": 0.08,
                  "hit": 0.05
                }
              },
              "C": 0.63,
              "D": {
                "irrelevant": 0.0,
                "no": 0.01,
                "yes": 0.99
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.05"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男はスープを飲んで、何か別のものを思い出したんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.1761964480392635,
      "judge_s": 1.1761964480392635,
      "luna_s": null,
      "total_s": 1.1762030370300636,
      "writer_s": 6.5889908000826836e-06
    }
  },
  {
    "case_id": "U28-e09",
    "record": {
      "comment_id": "U28-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "yes",
        "decision": "jev",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4991,
            "latency_s": 1.194946,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
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
                "point_0": {
                  "close": 0.01,
                  "hit": 0.01
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.32,
              "D": {
                "irrelevant": 0.15,
                "no": 0.02,
                "yes": 0.83
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい！じっくり考えてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "スープを出したのは、その店のシェフ本人ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.1953394019510597,
      "judge_s": 1.1953394019510597,
      "luna_s": null,
      "total_s": 1.195344883017242,
      "writer_s": 5.481066182255745e-06
    }
  },
  {
    "case_id": "U28-e10",
    "record": {
      "comment_id": "U28-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "no",
        "decision": "jev",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "guess_demoted": true,
            "input_tokens": 4979,
            "latency_s": 1.292932,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
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
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.05,
                  "hit": 0.03
                },
                "point_1": {
                  "close": 0.04,
                  "hit": 0.01
                }
              },
              "C": 0.66,
              "D": {
                "irrelevant": 0.36,
                "no": 0.64,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "いいえ。次の質問も待ってるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は昔、ウミガメを飼っていたんでしょか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.293358686962165,
      "judge_s": 1.293358686962165,
      "luna_s": null,
      "total_s": 1.2933632669737563,
      "writer_s": 4.5800115913152695e-06
    }
  },
  {
    "case_id": "U28-e11",
    "record": {
      "comment_id": "U28-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "q_multi"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "input_tokens": 2167,
            "latency_s": 0.564786,
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
                "q_multi": 0.93,
                "q_open": 0.0,
                "q_yesno": 0.07
              },
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_multi",
          "reason": "段A=question→q_multi"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "順番に 1 つずつ聞いてね😌"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は過去にウミガメを食べたことがあるの？その時の出来事を思い出したの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.5650152310263366,
      "judge_s": 0.5650152310263366,
      "luna_s": null,
      "total_s": 0.565021789050661,
      "writer_s": 6.558024324476719e-06
    }
  },
  {
    "case_id": "U28-e12",
    "record": {
      "comment_id": "U28-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "q_multi"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "input_tokens": 2155,
            "latency_s": 0.581408,
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
                "guess": 0.92,
                "question": 0.08
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
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "質問は 1 つずつコメントしてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "スープの味が記憶と違ったの？本物だと聞いて何かに気づいたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.5815982650965452,
      "judge_s": 0.5815982650965452,
      "luna_s": null,
      "total_s": 0.5816042650258169,
      "writer_s": 5.999929271638393e-06
    }
  },
  {
    "case_id": "U28-e13",
    "record": {
      "comment_id": "U28-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 2660,
            "latency_s": 1.009554,
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
                "guess": 0.02,
                "question": 0.98
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
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい・いいえで答えられる形で聞き直してね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男はなぜ本物のウミガメかどうか確かめたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.009796482976526,
      "judge_s": 1.009796482976526,
      "luna_s": null,
      "total_s": 1.0098019109573215,
      "writer_s": 5.427980795502663e-06
    }
  },
  {
    "case_id": "U28-e14",
    "record": {
      "comment_id": "U28-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 2664,
            "latency_s": 0.800219,
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
                "guess": 0.64,
                "question": 0.36
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
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "形を変えて、はい・いいえで聞いてみようか😉"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "スープを飲んだとき、男は何を思い出したんでしょう？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.8004797300091013,
      "judge_s": 0.8004797300091013,
      "luna_s": null,
      "total_s": 0.8004850540310144,
      "writer_s": 5.32402191311121e-06
    }
  },
  {
    "case_id": "U28-e15",
    "record": {
      "comment_id": "U28-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 2672,
            "latency_s": 0.802458,
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
                "guess": 0.09,
                "question": 0.91
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
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "その聞き方だと答えにくいな。はい・いいえで聞いてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男が泣き崩れるまでに、どんな過去があったんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.8026870120083913,
      "judge_s": 0.8026870120083913,
      "luna_s": null,
      "total_s": 0.8026919930707663,
      "writer_s": 4.98106237500906e-06
    }
  },
  {
    "case_id": "U28-e16",
    "record": {
      "comment_id": "U28-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "guess_correct"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 4055,
            "latency_s": 0.846977,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 209,
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
              "A_bare": 0.03,
              "B": {
                "point_0": {
                  "close": 0.87,
                  "hit": 0.78
                },
                "point_1": {
                  "close": 0.9800000000000001,
                  "hit": 0.93
                }
              },
              "B2": 0.1
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.78, 矛盾=0.10"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！男は遭難中、ウミガメのスープだと言われて亡くなった仲間の肉を飲んでいた。本物の味でそれに気づいた。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "昔ウミガメのスープだと言われて飲んだものが、仲間の肉だったってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.8472623070701957,
      "judge_s": 0.8472623070701957,
      "luna_s": null,
      "total_s": 0.8472647920716554,
      "writer_s": 2.4850014597177505e-06
    }
  },
  {
    "case_id": "U28-e17",
    "record": {
      "comment_id": "U28-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "guess_correct"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 4123,
            "latency_s": 0.791347,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 209,
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
                  "hit": 0.82
                },
                "point_1": {
                  "close": 0.99,
                  "hit": 0.96
                }
              },
              "B2": 0.08
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.82, 矛盾=0.08"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！男は遭難中、ウミガメのスープだと言われて亡くなった仲間の肉を飲んでいた。本物の味でそれに気づいた。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "昔、仲間の肉をウミガメのスープだと言われて飲んだんだね。本物の味が違って、あの時の嘘に気づいたのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.7915726359933615,
      "judge_s": 0.7915726359933615,
      "luna_s": null,
      "total_s": 0.7915740089956671,
      "writer_s": 1.3730023056268692e-06
    }
  },
  {
    "case_id": "U28-e18",
    "record": {
      "comment_id": "U28-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "guess_close"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "input_tokens": 2745,
            "latency_s": 0.598453,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 187,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.98,
                "reaction": 0.02,
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
                  "hit": 0.94
                },
                "point_1": {
                  "close": 0.08,
                  "hit": 0.05
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.05"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "惜しい！質問で確かめてみるといいよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "漂流していたとき、仲間からウミガメのスープだと言われて飲んだことがあったんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.5985966129228473,
      "judge_s": 0.5985966129228473,
      "luna_s": null,
      "total_s": 0.5986018688417971,
      "writer_s": 5.255918949842453e-06
    }
  },
  {
    "case_id": "U28-e19",
    "record": {
      "comment_id": "U28-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "guess_close"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 5,
            "input_tokens": 4706,
            "latency_s": 1.225198,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 255,
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
                "q_multi": 0.38,
                "q_open": 0.01,
                "q_yesno": 0.61
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.8600000000000001,
                  "hit": 0.81
                },
                "point_1": {
                  "close": 0.94,
                  "hit": 0.88
                }
              },
              "B2": 0.84
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=question→guess_close, 要点最低=0.81, 矛盾=0.84"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "惜しい！あきらめずに続けてね🙌"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "仲間の肉をウミガメのスープだと言われて飲んだんだね。でもそのとき仲間はみんな助かって、あとで一緒に帰れたのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.225484092021361,
      "judge_s": 1.225484092021361,
      "luna_s": null,
      "total_s": 1.2254890800686553,
      "writer_s": 4.988047294318676e-06
    }
  },
  {
    "case_id": "U28-e20",
    "record": {
      "comment_id": "U28-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "no",
        "decision": "jev",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "guess_demoted": true,
            "input_tokens": 5063,
            "latency_s": 1.274779,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
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
                "q_open": 0.14,
                "q_yesno": 0.83
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.06,
                  "hit": 0.04
                },
                "point_1": {
                  "close": 0.06,
                  "hit": 0.02
                }
              },
              "C": 0.45,
              "D": {
                "irrelevant": 0.0,
                "no": 1.0,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "いいえ。次の質問も待ってるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男はウミガメが大好きで、食べてしまったことが悲しくて泣いたんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.2750442549586296,
      "judge_s": 1.2750442549586296,
      "luna_s": null,
      "total_s": 1.2750492139020935,
      "writer_s": 4.958943463861942e-06
    }
  },
  {
    "case_id": "U28-e21",
    "record": {
      "comment_id": "U28-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "guess_close"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "input_tokens": 2760,
            "latency_s": 0.623717,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 187,
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
                "point_0": {
                  "close": 0.08,
                  "hit": 0.04
                },
                "point_1": {
                  "close": 0.31000000000000005,
                  "hit": 0.03
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.03"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "惜しい！質問で確かめてみるといいよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "子どものころに飼っていたカメがこのスープに使われたと思い込んで、悲しくなったんだと思う。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.6239369170507416,
      "judge_s": 0.6239369170507416,
      "luna_s": null,
      "total_s": 0.6239415410673246,
      "writer_s": 4.624016582965851e-06
    }
  },
  {
    "case_id": "U28-k01",
    "record": {
      "comment_id": "U28-k01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "guess_correct"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 4083,
            "latency_s": 0.89239,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 209,
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
                  "close": 0.8700000000000001,
                  "hit": 0.81
                },
                "point_1": {
                  "close": 0.9600000000000001,
                  "hit": 0.91
                }
              },
              "B2": 0.07
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.81, 矛盾=0.07"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！男は遭難中、ウミガメのスープだと言われて亡くなった仲間の肉を飲んでいた。本物の味でそれに気づいた。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "漂流中に亀のスープと聞かされて口にした一杯は、実は仲間の肉から作られてたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.8926903021056205,
      "judge_s": 0.8926903021056205,
      "luna_s": null,
      "total_s": 0.892691747052595,
      "writer_s": 1.444946974515915e-06
    }
  },
  {
    "case_id": "U28-k02",
    "record": {
      "comment_id": "U28-k02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "guess_correct"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 4087,
            "latency_s": 0.851566,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 209,
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
                  "close": 0.7899999999999999,
                  "hit": 0.7
                },
                "point_1": {
                  "close": 0.99,
                  "hit": 0.99
                }
              },
              "B2": 0.09
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.70, 矛盾=0.09"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！男は遭難中、ウミガメのスープだと言われて亡くなった仲間の肉を飲んでいた。本物の味でそれに気づいた。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "漂流中に亀の汁だと渡されて飲んだ一杯は仲間の肉で、男は正体に後から気づいたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.8519321599742398,
      "judge_s": 0.8519321599742398,
      "luna_s": null,
      "total_s": 0.8519335889723152,
      "writer_s": 1.4289980754256248e-06
    }
  },
  {
    "case_id": "U28-k03",
    "record": {
      "comment_id": "U28-k03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "guess_close"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "input_tokens": 2754,
            "latency_s": 0.724117,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 187,
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
                "point_0": {
                  "close": 0.9400000000000001,
                  "hit": 0.91
                },
                "point_1": {
                  "close": 0.96,
                  "hit": 0.02
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.02"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "惜しい！あきらめずに続けてね🙌"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "漂流中、ウミガメの汁だと説明されて飲んだけど、材料は口にしてはいけないものだったんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.7243206239072606,
      "judge_s": 0.7243206239072606,
      "luna_s": null,
      "total_s": 0.7243257159134373,
      "writer_s": 5.092006176710129e-06
    }
  },
  {
    "case_id": "U28-k04",
    "record": {
      "comment_id": "U28-k04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "guess_close"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 4099,
            "latency_s": 0.821332,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 209,
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
                  "close": 0.9600000000000001,
                  "hit": 0.91
                },
                "point_1": {
                  "close": 0.97,
                  "hit": 0.96
                }
              },
              "B2": 0.95
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.91, 矛盾=0.95"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "惜しい！あきらめずに続けてね🙌"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "以前、亀のスープだと言われて飲んだのは仲間の肉だった。でも漂流仲間は全員無事に帰れたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.8215938700595871,
      "judge_s": 0.8215938700595871,
      "luna_s": null,
      "total_s": 0.8215988989686593,
      "writer_s": 5.02890907227993e-06
    }
  },
  {
    "case_id": "U28-k05",
    "record": {
      "comment_id": "U28-k05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "guess_close"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "input_tokens": 2721,
            "latency_s": 0.544593,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 187,
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
                  "close": 0.9,
                  "hit": 0.1
                },
                "point_1": {
                  "close": 0.04,
                  "hit": 0.02
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.02"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "惜しい！質問で確かめてみるといいよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は昔もウミガメの汁を飲み、今のものとは味が違うと感じたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.5448385929921642,
      "judge_s": 0.5448385929921642,
      "luna_s": null,
      "total_s": 0.5448429629905149,
      "writer_s": 4.369998350739479e-06
    }
  },
  {
    "case_id": "U28-k06",
    "record": {
      "comment_id": "U28-k06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "guess_wrong"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "guess_demoted": true,
            "input_tokens": 3289,
            "latency_s": 0.897773,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 231,
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
                "q_open": 0.8,
                "q_yesno": 0.18
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.09,
                  "hit": 0.05
                },
                "point_1": {
                  "close": 0.05,
                  "hit": 0.02
                }
              }
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.02"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "残念、はずれだよ。また考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "今日の椀は偽物で、シェフが男の昔話を信じ込ませるために嘘をついたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.8980176990153268,
      "judge_s": 0.8980176990153268,
      "luna_s": null,
      "total_s": 0.8980230810120702,
      "writer_s": 5.381996743381023e-06
    }
  },
  {
    "case_id": "U28-t01",
    "record": {
      "comment_id": "U28-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "仲間の肉",
          "debug": {
            "calls": 1,
            "input_tokens": 929,
            "latency_s": 0.194052,
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
              "A_bare": 0.85
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.85"
        },
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "仲間の肉が何のことか、もう少し詳しく教えて！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "仲間の肉？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.19417385896667838,
      "judge_s": 0.19417385896667838,
      "luna_s": null,
      "total_s": 0.19418175297323614,
      "writer_s": 7.894006557762623e-06
    }
  },
  {
    "case_id": "U28-t02",
    "record": {
      "comment_id": "U28-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "レモン",
          "debug": {
            "calls": 1,
            "input_tokens": 927,
            "latency_s": 0.192732,
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
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "レモンがどうしたのか聞かせてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "レモン",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.19281693699304014,
      "judge_s": 0.19281693699304014,
      "luna_s": null,
      "total_s": 0.19282220106106251,
      "writer_s": 5.2640680223703384e-06
    }
  },
  {
    "case_id": "c-ask_howto-04",
    "record": {
      "comment_id": "c-ask_howto-04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "ask_howto"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1431,
            "latency_s": 0.509273,
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
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "コメントで質問すると、はい・いいえで返事が来るよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "質問したら返事もらえるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.5093893070006743,
      "judge_s": 0.5093893070006743,
      "luna_s": null,
      "total_s": 0.5093949679285288,
      "writer_s": 5.660927854478359e-06
    }
  },
  {
    "case_id": "c-cheer-03",
    "record": {
      "comment_id": "c-cheer-03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "cheer"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1588,
            "latency_s": 0.430817,
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
                "cheer": 0.92,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.02,
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
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "ありがとう！明日も出すからね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "更新たのしみにしてる〜",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.4309668919304386,
      "judge_s": 0.4309668919304386,
      "luna_s": null,
      "total_s": 0.4309713098919019,
      "writer_s": 4.417961463332176e-06
    }
  },
  {
    "case_id": "c-complaint-02",
    "record": {
      "comment_id": "c-complaint-02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "complaint"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1598,
            "latency_s": 0.434761,
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
                "complaint": 0.6,
                "greeting": 0.0,
                "impression": 0.38,
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
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "知らせてくれてありがとう。確認するね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "前の投稿と設定が被ってる気がする",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.43483744096010923,
      "judge_s": 0.43483744096010923,
      "luna_s": null,
      "total_s": 0.43484217196237296,
      "writer_s": 4.731002263724804e-06
    }
  },
  {
    "case_id": "c-troll-01",
    "record": {
      "comment_id": "c-troll-01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "troll"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1472,
            "latency_s": 0.44336,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
            "probabilities": {
              "A1": {
                "inappropriate": 0.87,
                "other": 0.0,
                "question_or_guess": 0.01,
                "reaction": 0.12,
                "request": 0.0
              },
              "A2": {
                "abuse": 0.0,
                "personal_info": 0.0,
                "spam": 0.0,
                "troll": 1.0
              },
              "A_bare": 0.46
            }
          },
          "error": null,
          "kind": "troll",
          "reason": "段A=inappropriate→troll"
        },
        "luna": null
      },
      "media_id": "local-U28",
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
      "text": "ぬぬぬぬぬ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 0.4434915150050074,
      "judge_s": 0.4434915150050074,
      "luna_s": null,
      "total_s": 0.4434966070111841,
      "writer_s": 5.092006176710129e-06
    }
  },
  {
    "case_id": "c-spam-05",
    "record": {
      "comment_id": "c-spam-05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "jev",
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
        "luna": null
      },
      "media_id": "local-U28",
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
      "text": "無料プレゼント応募は固定リンクから→ https://example.invalid/gift",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "jev_s": 1.2101954780519009e-05,
      "judge_s": 1.2101954780519009e-05,
      "luna_s": null,
      "total_s": 1.3155979104340076e-05,
      "writer_s": 1.0540243238210678e-06
    }
  }
];
