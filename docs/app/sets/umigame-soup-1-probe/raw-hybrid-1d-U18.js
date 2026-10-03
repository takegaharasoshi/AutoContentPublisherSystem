window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["hybrid-1d/U18"] = [
  {
    "case_id": "U18-e01",
    "record": {
      "comment_id": "U18-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4044,
            "latency_s": 1.246634,
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
                "guess": 0.09,
                "question": 0.91
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.03,
                "point_1": 0.02
              },
              "C": 0.38,
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
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 208,
            "finish_reason": "stop",
            "latency_s": 7.674695,
            "model": "gpt-6-luna",
            "prompt_tokens": 2806,
            "reasoning_tokens": 134
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、約束は口約束ではなく書かれたものとされています。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "約束は口約束だったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.247081759996945,
      "judge_s": 7.67474801899516,
      "luna_s": 7.67474801899516,
      "total_s": 9.19112512198626,
      "writer_s": 1.5163771029911004
    }
  },
  {
    "case_id": "U18-e02",
    "record": {
      "comment_id": "U18-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4080,
            "latency_s": 1.256542,
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
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.05,
              "B": {
                "point_0": 0.25,
                "point_1": 0.08
              },
              "C": 0.35,
              "D": {
                "irrelevant": 0.0,
                "no": 0.0,
                "yes": 1.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.08"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 212,
            "finish_reason": "stop",
            "latency_s": 2.028965,
            "model": "gpt-6-luna",
            "prompt_tokens": 2810,
            "reasoning_tokens": 138
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、白紙に戻ったのは目に見える形のあるものとされています。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！次は何を聞こうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "白紙になったのは、目に見えるもの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2569363130023703,
      "judge_s": 2.0290263820206746,
      "luna_s": 2.0290263820206746,
      "total_s": 3.5391404130205046,
      "writer_s": 1.51011403099983
    }
  },
  {
    "case_id": "U18-e03",
    "record": {
      "comment_id": "U18-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4044,
            "latency_s": 1.154122,
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
                "guess": 0.89,
                "question": 0.11
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01,
                "point_1": 0.01
              },
              "C": 0.25,
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
            "completion_tokens": 139,
            "finish_reason": "stop",
            "latency_s": 17.418815,
            "model": "gpt-6-luna",
            "prompt_tokens": 2806,
            "reasoning_tokens": 72
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、2人はけんかをしていないとされています。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "ふたりはけんかしてた？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1543928330065683,
      "judge_s": 17.41886607700144,
      "luna_s": 17.41886607700144,
      "total_s": 24.945015841018176,
      "writer_s": 7.526149764016736
    }
  },
  {
    "case_id": "U18-e04",
    "record": {
      "comment_id": "U18-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4044,
            "latency_s": 1.206025,
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
                "guess": 0.89,
                "question": 0.11
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.07,
              "B": {
                "point_0": 0.03,
                "point_1": 0.01
              },
              "C": 0.53,
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
            "completion_tokens": 126,
            "finish_reason": "stop",
            "latency_s": 1.884678,
            "model": "gpt-6-luna",
            "prompt_tokens": 2807,
            "reasoning_tokens": 68
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、夏の天気（夕立）が関係するとされています。"
        }
      },
      "media_id": "local-U18",
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
      "text": "夏の夕立が関係してる？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2063765589846298,
      "judge_s": 1.8847311100107618,
      "luna_s": 1.8847311100107618,
      "total_s": 2.929434874036815,
      "writer_s": 1.0447037640260532
    }
  },
  {
    "case_id": "U18-e05",
    "record": {
      "comment_id": "U18-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4056,
            "latency_s": 1.251219,
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
                "guess": 0.95,
                "question": 0.05
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.04,
                "point_1": 0.03
              },
              "C": 0.27,
              "D": {
                "irrelevant": 0.0,
                "no": 0.0,
                "yes": 1.0
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
            "completion_tokens": 241,
            "finish_reason": "stop",
            "latency_s": 2.401865,
            "model": "gpt-6-luna",
            "prompt_tokens": 2808,
            "reasoning_tokens": 171
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、濡れたものを乾かしたことが関係するとあります。"
        }
      },
      "media_id": "local-U18",
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
      "text": "濡れたものを乾かしたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2515396400121972,
      "judge_s": 2.401917635987047,
      "luna_s": 2.401917635987047,
      "total_s": 5.640775856008986,
      "writer_s": 3.238858220021939
    }
  },
  {
    "case_id": "U18-e06",
    "record": {
      "comment_id": "U18-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4056,
            "latency_s": 1.151114,
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
                "guess": 0.94,
                "question": 0.06
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.06,
              "B": {
                "point_0": 0.08,
                "point_1": 0.02
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
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 194,
            "finish_reason": "stop",
            "latency_s": 2.280117,
            "model": "gpt-6-luna",
            "prompt_tokens": 2806,
            "reasoning_tokens": 131
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "約束は取り消されていないと確定しています。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "約束そのものを取り消した？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1514055469888262,
      "judge_s": 2.2801718300033826,
      "luna_s": 2.2801718300033826,
      "total_s": 3.9780856930010486,
      "writer_s": 1.697913862997666
    }
  },
  {
    "case_id": "U18-e07",
    "record": {
      "comment_id": "U18-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4068,
            "latency_s": 1.208596,
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
                "q_multi": 0.01,
                "q_open": 0.02,
                "q_yesno": 0.97
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.02,
                "point_1": 0.01
              },
              "C": 0.34,
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
            "completion_tokens": 183,
            "finish_reason": "stop",
            "latency_s": 17.444307,
            "model": "gpt-6-luna",
            "prompt_tokens": 2810,
            "reasoning_tokens": 110
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、約束の中身は二人とも覚えていたとあります。"
        }
      },
      "media_id": "local-U18",
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
      "text": "約束の中身は二人とも覚えてた？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2089051569928415,
      "judge_s": 17.444354355015093,
      "luna_s": 17.444354355015093,
      "total_s": 18.34150867702556,
      "writer_s": 0.897154322010465
    }
  },
  {
    "case_id": "U18-e08",
    "record": {
      "comment_id": "U18-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4044,
            "latency_s": 1.133595,
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
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.06,
              "B": {
                "point_0": 0.03,
                "point_1": 0.02
              },
              "C": 0.3,
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
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 290,
            "finish_reason": "stop",
            "latency_s": 2.929245,
            "model": "gpt-6-luna",
            "prompt_tokens": 2805,
            "reasoning_tokens": 215
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、起きたことは誰かのいたずらではなく事故とされています。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "誰かのいたずらだった？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1339430539810564,
      "judge_s": 2.929303619021084,
      "luna_s": 2.929303619021084,
      "total_s": 6.193524597998476,
      "writer_s": 3.2642209789773915
    }
  },
  {
    "case_id": "U18-e09",
    "record": {
      "comment_id": "U18-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4068,
            "latency_s": 1.164919,
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
                "guess": 0.08,
                "question": 0.92
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01,
                "point_1": 0.01
              },
              "C": 0.83,
              "D": {
                "irrelevant": 0.03,
                "no": 0.0,
                "yes": 0.97
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
            "completion_tokens": 170,
            "finish_reason": "stop",
            "latency_s": 7.099636,
            "model": "gpt-6-luna",
            "prompt_tokens": 2810,
            "reasoning_tokens": 103
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "真相で、約束は後日きちんと果たされたと示されています。"
        }
      },
      "media_id": "local-U18",
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
      "text": "二人は後日その約束を果たした？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.165260331996251,
      "judge_s": 7.099671295989538,
      "luna_s": 7.099671295989538,
      "total_s": 10.2696377520042,
      "writer_s": 3.169966456014663
    }
  },
  {
    "case_id": "U18-e10",
    "record": {
      "comment_id": "U18-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4092,
            "latency_s": 1.224366,
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
                "guess": 0.02,
                "question": 0.98
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.01,
                "point_1": 0.01
              },
              "C": 0.48,
              "D": {
                "irrelevant": 0.02,
                "no": 0.98,
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
            "completion_tokens": 171,
            "finish_reason": "stop",
            "latency_s": 2.195319,
            "model": "gpt-6-luna",
            "prompt_tokens": 2814,
            "reasoning_tokens": 97
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、二人の年齢は問題に関係ないとされています。"
        }
      },
      "media_id": "local-U18",
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
      "text": "二人の年齢って謎を解くのに関係ある？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2248148870130535,
      "judge_s": 2.195372871996369,
      "luna_s": 2.195372871996369,
      "total_s": 9.933989858982386,
      "writer_s": 7.738616986986017
    }
  },
  {
    "case_id": "U18-e11",
    "record": {
      "comment_id": "U18-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2122,
            "latency_s": 0.665388,
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
                "guess": 0.61,
                "question": 0.39
              },
              "A2": {
                "q_multi": 0.97,
                "q_open": 0.02,
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
            "completion_tokens": 171,
            "finish_reason": "stop",
            "latency_s": 1.89542,
            "model": "gpt-6-luna",
            "prompt_tokens": 2813,
            "reasoning_tokens": 96
          },
          "error": null,
          "kind": "q_multi",
          "reason": "濡れたかの質問と、その後どうしたかの質問が二つあります。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。まずはどちらか聞いてみようか☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "雨で何か濡れたの？そのあとどうしたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.6656305569922552,
      "judge_s": 1.895472628006246,
      "luna_s": 1.895472628006246,
      "total_s": 3.400436439027544,
      "writer_s": 1.5049638110212982
    }
  },
  {
    "case_id": "U18-e12",
    "record": {
      "comment_id": "U18-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2143,
            "latency_s": 0.649156,
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
                "guess": 0.28,
                "question": 0.72
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
            "latency_s": 1.825743,
            "model": "gpt-6-luna",
            "prompt_tokens": 2817,
            "reasoning_tokens": 52
          },
          "error": null,
          "kind": "q_multi",
          "reason": "約束の取り消しと後日の実行について、質問が二つあります。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問は1つずつコメントしてね。順番に考えていこうか☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "約束は取り消されたの？それでも二人はあとで実行したの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.6493267449841369,
      "judge_s": 1.8257849109941162,
      "luna_s": 1.8257849109941162,
      "total_s": 3.360765285004163,
      "writer_s": 1.534980374010047
    }
  },
  {
    "case_id": "U18-e13",
    "record": {
      "comment_id": "U18-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2668,
            "latency_s": 0.863133,
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
                "guess": 0.04,
                "question": 0.96
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.99,
                "q_yesno": 0.01
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
            "completion_tokens": 168,
            "finish_reason": "stop",
            "latency_s": 2.938701,
            "model": "gpt-6-luna",
            "prompt_tokens": 2819,
            "reasoning_tokens": 87
          },
          "error": null,
          "kind": "q_open",
          "reason": "「なぜ」と理由を尋ねる質問で、はい／いいえでは答えられません。"
        }
      },
      "media_id": "local-U18",
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
      "shadow_mismatch": false,
      "text": "なぜ約束が白紙に戻ったのに、二人は悲しまなかったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.8632922419928946,
      "judge_s": 2.9389056939980946,
      "luna_s": 2.9389056939980946,
      "total_s": 6.843921713996679,
      "writer_s": 3.905016019998584
    }
  },
  {
    "case_id": "U18-e14",
    "record": {
      "comment_id": "U18-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2632,
            "latency_s": 0.850119,
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
                "guess": 0.05,
                "question": 0.95
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.99,
                "q_yesno": 0.01
              },
              "A3": 0.04,
              "A_bare": 0.02
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
            "completion_tokens": 179,
            "finish_reason": "stop",
            "latency_s": 2.084798,
            "model": "gpt-6-luna",
            "prompt_tokens": 2811,
            "reasoning_tokens": 91
          },
          "error": null,
          "kind": "q_open",
          "reason": "「どうして」と理由を尋ねており、はい／いいえでは答えられないためです。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "「後日その約束を果たせたの？」のように、はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "どうして後日その約束を果たせたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.8503491289739031,
      "judge_s": 2.0848565100168344,
      "luna_s": 2.0848565100168344,
      "total_s": 4.867236124991905,
      "writer_s": 2.7823796149750706
    }
  },
  {
    "case_id": "U18-e15",
    "record": {
      "comment_id": "U18-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2608,
            "latency_s": 0.805605,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 178,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.97,
                "reaction": 0.03,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.24,
                "question": 0.76
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.17,
                "q_yesno": 0.83
              },
              "A3": 0.39,
              "A_bare": 0.03
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.39"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 433,
            "finish_reason": "stop",
            "latency_s": 8.62513,
            "model": "gpt-6-luna",
            "prompt_tokens": 2805,
            "reasoning_tokens": 343
          },
          "error": null,
          "kind": "q_open",
          "reason": "「それ」の指す対象が一つに定まらず、質問の内容を特定できません。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "「それ」が何か分かるようにして、はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "それはまだ覚えてるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.8057807880104519,
      "judge_s": 8.625220488000195,
      "luna_s": 8.625220488000195,
      "total_s": 13.676390008011367,
      "writer_s": 5.051169520011172
    }
  },
  {
    "case_id": "U18-e16",
    "record": {
      "comment_id": "U18-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2229,
            "latency_s": 0.547307,
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
                "point_0": 0.97,
                "point_1": 0.98
              }
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.97"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 252,
            "finish_reason": "stop",
            "latency_s": 17.840958,
            "model": "gpt-6-luna",
            "prompt_tokens": 2863,
            "reasoning_tokens": 141
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "文字が消せるペンで書かれ、熱で消えたことまで言い当てています。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！夕立で濡れた手紙をドライヤーで乾かし、消せるペンの文字が消えた。2人は約束を書き直して果たした。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男が消せるボールペンで書いた手紙が夕立で濡れ、女がドライヤーで乾かした熱で文字が消えて白紙になった。二人は約束の中身を覚えていて書き直し、後日果たした。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.5474438139935955,
      "judge_s": 17.841158144001383,
      "luna_s": 17.841158144001383,
      "total_s": 17.84117290598806,
      "writer_s": 1.4761986676603556e-05
    }
  },
  {
    "case_id": "U18-e17",
    "record": {
      "comment_id": "U18-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2202,
            "latency_s": 0.572294,
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
                "guess": 0.99,
                "question": 0.01
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.95,
                "point_1": 0.96
              }
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.95"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 272,
            "finish_reason": "stop",
            "latency_s": 7.702009,
            "model": "gpt-6-luna",
            "prompt_tokens": 2853,
            "reasoning_tokens": 155
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "文字が消せるペンで書かれていたことと、約束を覚えて果たしたことを言い当てています。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！夕立で濡れた手紙をドライヤーで乾かし、消せるペンの文字が消えた。2人は約束を書き直して果たした。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "夕立で濡れた手紙をドライヤーで乾かしたら、消せるペンの文字が熱で消えた。でも二人とも約束は覚えていて、書き直して後日果たしたってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.5724241459975019,
      "judge_s": 7.70205202800571,
      "luna_s": 7.70205202800571,
      "total_s": 7.702057068992872,
      "writer_s": 5.040987161919475e-06
    }
  },
  {
    "case_id": "U18-e18",
    "record": {
      "comment_id": "U18-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2121,
            "latency_s": 0.586329,
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
                "point_1": 0.05
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.05"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 139,
            "finish_reason": "stop",
            "latency_s": 1.893612,
            "model": "gpt-6-luna",
            "prompt_tokens": 2831,
            "reasoning_tokens": 72
          },
          "error": null,
          "kind": "guess_close",
          "reason": "文字が消えたことと約束を覚えていた点は合っていますが、核心の一つが抜けています。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し推理を続けてみようか☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "雨に濡れた紙の文字が消えて白紙になったけど、二人は約束の内容を覚えていたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.5864877099811565,
      "judge_s": 1.893661993992282,
      "luna_s": 1.893661993992282,
      "total_s": 3.5316146969853435,
      "writer_s": 1.6379527029930614
    }
  },
  {
    "case_id": "U18-e19",
    "record": {
      "comment_id": "U18-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2109,
            "latency_s": 0.606829,
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
                "point_0": 0.86,
                "point_1": 0.15
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.15"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 263,
            "finish_reason": "stop",
            "latency_s": 2.803995,
            "model": "gpt-6-luna",
            "prompt_tokens": 2827,
            "reasoning_tokens": 190
          },
          "error": null,
          "kind": "guess_close",
          "reason": "紙が白紙になったことと約束が続いた点には触れていますが、コアの要点すべてには届いていません。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し推理を続けてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "約束は紙に書かれていて、白紙になったあと二人は同じ約束を続けたんじゃない？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.6070727650076151,
      "judge_s": 2.804041583003709,
      "luna_s": 2.804041583003709,
      "total_s": 10.26051916499273,
      "writer_s": 7.45647758198902
    }
  },
  {
    "case_id": "U18-e20",
    "record": {
      "comment_id": "U18-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2646,
            "latency_s": 0.762018,
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
                "q_multi": 0.04,
                "q_open": 0.73,
                "q_yesno": 0.23
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02,
                "point_1": 0.01
              }
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.01"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 193,
            "finish_reason": "stop",
            "latency_s": 2.382455,
            "model": "gpt-6-luna",
            "prompt_tokens": 2826,
            "reasoning_tokens": 126
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "約束を取り消したという推理で、文字が消えた仕掛けには触れていません。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。別の可能性も考えてみようか☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "二人が大げんかして約束を取り消し、仲直りしたあと別の約束をしたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.762275396991754,
      "judge_s": 2.382493249984691,
      "luna_s": 2.382493249984691,
      "total_s": 6.222123285988346,
      "writer_s": 3.839630036003655
    }
  },
  {
    "case_id": "U18-e21",
    "record": {
      "comment_id": "U18-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2658,
            "latency_s": 0.825603,
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
                "q_multi": 0.01,
                "q_open": 0.88,
                "q_yesno": 0.11
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.06,
                "point_1": 0.02
              }
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.02"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 325,
            "finish_reason": "stop",
            "latency_s": 18.435675,
            "model": "gpt-6-luna",
            "prompt_tokens": 2828,
            "reasoning_tokens": 256
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "紙が破られて諦めたという推理で、文字が消える仕掛けには触れていません。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。別の可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "約束を書いた紙を誰かに破られてしまい、二人は悲しくてそのまま諦めたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.825855182018131,
      "judge_s": 18.435726913972758,
      "luna_s": 18.435726913972758,
      "total_s": 19.609315883979434,
      "writer_s": 1.1735889700066764
    }
  },
  {
    "case_id": "U18-b22",
    "record": {
      "comment_id": "U18-b22",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4068,
            "latency_s": 1.235123,
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
                "guess": 0.02,
                "question": 0.98
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01,
                "point_1": 0.01
              },
              "C": 0.48,
              "D": {
                "irrelevant": 0.94,
                "no": 0.04,
                "yes": 0.02
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
            "completion_tokens": 486,
            "finish_reason": "stop",
            "latency_s": 9.585388,
            "model": "gpt-6-luna",
            "prompt_tokens": 2810,
            "reasoning_tokens": 413
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "約束の具体的な内容は、真相を解くうえで関係しません。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "2人は直接会う約束をしてたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2354681150172837,
      "judge_s": 9.58542070002295,
      "luna_s": 9.58542070002295,
      "total_s": 17.33578140102327,
      "writer_s": 7.750360701000318
    }
  },
  {
    "case_id": "U18-b23",
    "record": {
      "comment_id": "U18-b23",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4092,
            "latency_s": 1.361319,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 256,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.0,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.06,
                "question": 0.94
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.04,
                "q_yesno": 0.96
              },
              "A_bare": 0.04,
              "B": {
                "point_0": 0.04,
                "point_1": 0.02
              },
              "C": 0.45,
              "D": {
                "irrelevant": 0.0,
                "no": 0.16,
                "yes": 0.84
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
            "completion_tokens": 224,
            "finish_reason": "stop",
            "latency_s": 2.574657,
            "model": "gpt-6-luna",
            "prompt_tokens": 2811,
            "reasoning_tokens": 165
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "「白紙」は、紙の文字が消えてまっさらになったという意味です。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！紙が真っ白になったって意味だよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "「白紙」は紙が真っ白になったって意味？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.3615400569979101,
      "judge_s": 2.574686494015623,
      "luna_s": 2.574686494015623,
      "total_s": 4.422970943007385,
      "writer_s": 1.8482844489917625
    }
  },
  {
    "case_id": "U18-b24",
    "record": {
      "comment_id": "U18-b24",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4080,
            "latency_s": 1.335031,
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
                "guess": 0.57,
                "question": 0.43
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.02,
                "point_1": 0.01
              },
              "C": 0.26,
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
            "completion_tokens": 242,
            "finish_reason": "stop",
            "latency_s": 2.407893,
            "model": "gpt-6-luna",
            "prompt_tokens": 2811,
            "reasoning_tokens": 168
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "夏の夕立で、手紙が濡れる事故のような出来事が起きています。"
        }
      },
      "media_id": "local-U18",
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
      "text": "夏の日に何か予定外のことが起きた？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.3352627329877578,
      "judge_s": 2.407960895972792,
      "luna_s": 2.407960895972792,
      "total_s": 9.755118644970935,
      "writer_s": 7.347157748998143
    }
  },
  {
    "case_id": "U18-b25",
    "record": {
      "comment_id": "U18-b25",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4038,
            "latency_s": 1.20942,
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
                "guess": 0.04,
                "question": 0.96
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
              "C": 0.21,
              "D": {
                "irrelevant": 0.97,
                "no": 0.02,
                "yes": 0.01
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
            "completion_tokens": 325,
            "finish_reason": "stop",
            "latency_s": 8.705162,
            "model": "gpt-6-luna",
            "prompt_tokens": 2806,
            "reasoning_tokens": 249
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "恋人かどうかは真相に関係せず、確定事実にもありません。"
        }
      },
      "media_id": "local-U18",
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
      "shadow_mismatch": false,
      "text": "2人は恋人同士なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2096238429949153,
      "judge_s": 8.705210085987346,
      "luna_s": 8.705210085987346,
      "total_s": 16.807878749998054,
      "writer_s": 8.102668664010707
    }
  },
  {
    "case_id": "U18-b26",
    "record": {
      "comment_id": "U18-b26",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4062,
            "latency_s": 1.207291,
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
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02,
                "point_1": 0.01
              },
              "C": 0.5,
              "D": {
                "irrelevant": 0.02,
                "no": 0.73,
                "yes": 0.25
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
            "completion_tokens": 360,
            "finish_reason": "stop",
            "latency_s": 3.458659,
            "model": "gpt-6-luna",
            "prompt_tokens": 2806,
            "reasoning_tokens": 288
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "約束が延期だけだったかを尋ねる質問です。真相では延期ではありません。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ほかのことも聞いてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "約束は延期になっただけなの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2075214790238533,
      "judge_s": 3.458702590985922,
      "luna_s": 3.458702590985922,
      "total_s": 4.780339983990416,
      "writer_s": 1.3216373930044938
    }
  },
  {
    "case_id": "U18-b27",
    "record": {
      "comment_id": "U18-b27",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4062,
            "latency_s": 2.21686,
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
                "guess": 0.0,
                "question": 1.0
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
              "C": 0.58,
              "D": {
                "irrelevant": 0.08,
                "no": 0.71,
                "yes": 0.21
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
            "completion_tokens": 345,
            "finish_reason": "stop",
            "latency_s": 8.478105,
            "model": "gpt-6-luna",
            "prompt_tokens": 2809,
            "reasoning_tokens": 273
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "約束の中身は問題に関係ないと確定しています。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。次はどんなことを聞こうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "約束の内容は夏に関係あるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 2.217083775001811,
      "judge_s": 8.478131440002471,
      "luna_s": 8.478131440002471,
      "total_s": 10.254879118991084,
      "writer_s": 1.7767476789886132
    }
  },
  {
    "case_id": "U18-b28",
    "record": {
      "comment_id": "U18-b28",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4032,
            "latency_s": 1.171499,
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
                "guess": 0.66,
                "question": 0.34
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
              "C": 0.39,
              "D": {
                "irrelevant": 0.92,
                "no": 0.08,
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
            "completion_tokens": 238,
            "finish_reason": "stop",
            "latency_s": 19.128072,
            "model": "gpt-6-luna",
            "prompt_tokens": 2805,
            "reasoning_tokens": 178
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "2人の年齢は真相に関係しないと確定しています。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ほかのことも聞いてごらん"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "2人は子どもなの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1717464539979119,
      "judge_s": 19.128267923981184,
      "luna_s": 19.128267923981184,
      "total_s": 22.971671333973063,
      "writer_s": 3.843403409991879
    }
  },
  {
    "case_id": "U18-t01",
    "record": {
      "comment_id": "U18-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "8832e6127fa7",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "消せるボールペン",
          "debug": {
            "calls": 1,
            "input_tokens": 933,
            "latency_s": 0.208681,
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
          "bare_term": "消せるボールペン",
          "debug": {
            "completion_tokens": 374,
            "finish_reason": "stop",
            "latency_s": 3.464724,
            "model": "gpt-6-luna",
            "prompt_tokens": 2805,
            "reasoning_tokens": 289
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句だけのコメントなので、q_openと判定しました。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "何が消せるボールペンなのか教えてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "消せるボールペン？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.20876085897907615,
      "judge_s": 3.464779152011033,
      "luna_s": 3.464779152011033,
      "total_s": 6.271799187990837,
      "writer_s": 2.8070200359798037
    }
  },
  {
    "case_id": "U18-t02",
    "record": {
      "comment_id": "U18-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "8832e6127fa7",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "バスケットボール",
          "debug": {
            "calls": 1,
            "input_tokens": 932,
            "latency_s": 0.188468,
            "model": "jev-latest",
            "output_tokens": 78,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.07,
                "question_or_guess": 0.93,
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
          "bare_term": "バスケットボール",
          "debug": {
            "completion_tokens": 143,
            "finish_reason": "stop",
            "latency_s": 1.946557,
            "model": "gpt-6-luna",
            "prompt_tokens": 2802,
            "reasoning_tokens": 67
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句だけのコメントなので、質問として聞き直してもらいます。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "バスケットボールが何のことか、もう少し詳しく教えて！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "バスケットボール",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.18856769098783843,
      "judge_s": 1.9466156749986112,
      "luna_s": 1.9466156749986112,
      "total_s": 4.38302351499442,
      "writer_s": 2.436407839995809
    }
  },
  {
    "case_id": "c-ask_spoiler-01",
    "record": {
      "comment_id": "c-ask_spoiler-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "ask_spoiler"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1421,
            "latency_s": 0.435189,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 124,
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
                "ask_howto": 0.0,
                "ask_spoiler": 1.0
              },
              "A_bare": 0.11
            }
          },
          "error": null,
          "kind": "ask_spoiler",
          "reason": "段A=request→ask_spoiler"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 183,
            "finish_reason": "stop",
            "latency_s": 2.305026,
            "model": "gpt-6-luna",
            "prompt_tokens": 2803,
            "reasoning_tokens": 100
          },
          "error": null,
          "kind": "ask_spoiler",
          "reason": "答えそのものを教えてほしいという、ネタバレの依頼です。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問には答えられるけど、真相は教えられないよ。質問で少しずつ絞ってみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "答えだけ教えて〜",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.4353334339975845,
      "judge_s": 2.3050508910091594,
      "luna_s": 2.3050508910091594,
      "total_s": 6.0104054610128514,
      "writer_s": 3.705354570003692
    }
  },
  {
    "case_id": "c-impression-05",
    "record": {
      "comment_id": "c-impression-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "impression"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1584,
            "latency_s": 0.457083,
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
                "greeting": 0.0,
                "impression": 1.0,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.1
            }
          },
          "error": null,
          "kind": "impression",
          "reason": "段A=reaction→impression"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 138,
            "finish_reason": "stop",
            "latency_s": 17.891469,
            "model": "gpt-6-luna",
            "prompt_tokens": 2806,
            "reasoning_tokens": 84
          },
          "error": null,
          "kind": "impression",
          "reason": "問題の奥深さへの感想なので、感想として分類します。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "そう言ってもらえてうれしいよ☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "短いのに奥が深い！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.45722773601301014,
      "judge_s": 17.891522516001714,
      "luna_s": 17.891522516001714,
      "total_s": 18.89737813800457,
      "writer_s": 1.005855622002855
    }
  },
  {
    "case_id": "c-chat-04",
    "record": {
      "comment_id": "c-chat-04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "chat"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1592,
            "latency_s": 0.484244,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 148,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.01,
                "reaction": 0.99,
                "request": 0.0
              },
              "A2": {
                "chat": 0.95,
                "cheer": 0.0,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.05,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.05
            }
          },
          "error": null,
          "kind": "chat",
          "reason": "段A=reaction→chat"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 182,
            "finish_reason": "stop",
            "latency_s": 7.595393,
            "model": "gpt-6-luna",
            "prompt_tokens": 2807,
            "reasoning_tokens": 119
          },
          "error": null,
          "kind": "chat",
          "reason": "問題への推理や質問ではなく、週末についての雑談です。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ほんと、あっという間だね〜😌"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "週末ってあっという間だなー",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.48431980700115673,
      "judge_s": 7.595454788999632,
      "luna_s": 7.595454788999632,
      "total_s": 9.238339665025705,
      "writer_s": 1.6428848760260735
    }
  },
  {
    "case_id": "c-mention-03",
    "record": {
      "comment_id": "c-mention-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "mention"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1590,
            "latency_s": 0.4139,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 148,
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
                "greeting": 0.0,
                "impression": 0.0,
                "mention": 1.0,
                "request": 0.0
              },
              "A_bare": 0.09
            }
          },
          "error": null,
          "kind": "mention",
          "reason": "段A=reaction→mention"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 178,
            "finish_reason": "stop",
            "latency_s": 2.177687,
            "model": "gpt-6-luna",
            "prompt_tokens": 2805,
            "reasoning_tokens": 112
          },
          "error": null,
          "kind": "mention",
          "reason": "友人をタグ付けし、問題に関心を持ちそうだと伝えています。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "そうなんだね！ゆきさんも楽しんでいってね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "@yuki こういうの好きそう",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.41398896399186924,
      "judge_s": 2.177757922996534,
      "luna_s": 2.177757922996534,
      "total_s": 4.528017689008266,
      "writer_s": 2.3502597660117317
    }
  },
  {
    "case_id": "c-complaint-07",
    "record": {
      "comment_id": "c-complaint-07",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 1586,
            "latency_s": 0.37077,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 149,
            "probabilities": {
              "A1": {
                "inappropriate": 0.03,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.97,
                "request": 0.0
              },
              "A2": {
                "chat": 0.0,
                "cheer": 0.0,
                "complaint": 1.0,
                "greeting": 0.0,
                "impression": 0.0,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.12
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
            "completion_tokens": 142,
            "finish_reason": "stop",
            "latency_s": 1.940382,
            "model": "gpt-6-luna",
            "prompt_tokens": 2805,
            "reasoning_tokens": 79
          },
          "error": null,
          "kind": "complaint",
          "reason": "問題そのものをけなす内容なので、クレームとして扱います。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "コメントありがとう。確認するね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "バカみたいな問題だな",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.37084911300917156,
      "judge_s": 1.9404368329851422,
      "luna_s": 1.9404368329851422,
      "total_s": 3.3299028479668777,
      "writer_s": 1.3894660149817355
    }
  },
  {
    "case_id": "c-foreign-01",
    "record": {
      "comment_id": "c-foreign-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "foreign"
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
          "kind": "foreign",
          "reason": "段0規則: foreign"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 139,
            "finish_reason": "stop",
            "latency_s": 2.050661,
            "model": "gpt-6-luna",
            "prompt_tokens": 2801,
            "reasoning_tokens": 75
          },
          "error": null,
          "kind": "foreign",
          "reason": "日本語以外の英語コメントなので、foreignに分類します。"
        }
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "日本語で質問してね！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "That was fun!",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 5.4928008466959e-05,
      "judge_s": 2.0507182010042015,
      "luna_s": 2.0507182010042015,
      "total_s": 3.290536996006267,
      "writer_s": 1.2398187950020656
    }
  }
];
