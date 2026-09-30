window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["hybrid-1d/U13"] = [
  {
    "case_id": "U13-e01",
    "record": {
      "comment_id": "U13-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 4282,
            "latency_s": 2.244945,
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
                "guess": 0.04,
                "question": 0.96
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.03,
                "point_1": 0.01
              },
              "C": 0.42,
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
            "completion_tokens": 192,
            "finish_reason": "stop",
            "latency_s": 2.903854,
            "model": "gpt-6-luna",
            "prompt_tokens": 2953,
            "reasoning_tokens": 131
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実では、家のポストではなく集まりの場で手渡されています。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。男の家のポストに届いたの？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "手紙って男の家のポストに届いたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 2.2453060719999485,
      "judge_s": 2.903902743011713,
      "luna_s": 2.903902743011713,
      "total_s": 8.346917934017256,
      "writer_s": 5.443015191005543
    }
  },
  {
    "case_id": "U13-e02",
    "record": {
      "comment_id": "U13-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 4294,
            "latency_s": 1.21957,
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
                "guess": 0.88,
                "question": 0.12
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.04,
                "q_yesno": 0.96
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.03,
                "point_1": 0.02
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
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 297,
            "finish_reason": "stop",
            "latency_s": 4.40926,
            "model": "gpt-6-luna",
            "prompt_tokens": 2956,
            "reasoning_tokens": 229
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、配達に何十年もかかったのではないと示されています。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "郵便屋さんが何十年もかけて配達したの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.2199836840154603,
      "judge_s": 4.40928568597883,
      "luna_s": 4.40928568597883,
      "total_s": 8.21708688995568,
      "writer_s": 3.807801203976851
    }
  },
  {
    "case_id": "U13-e03",
    "record": {
      "comment_id": "U13-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 4270,
            "latency_s": 1.450611,
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
                "guess": 0.22,
                "question": 0.78
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.07,
                "point_1": 0.02
              },
              "C": 0.37,
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
            "completion_tokens": 173,
            "finish_reason": "stop",
            "latency_s": 2.821433,
            "model": "gpt-6-luna",
            "prompt_tokens": 2952,
            "reasoning_tokens": 99
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "学校行事で書かれたかを尋ねる一つの質問で、確定事実に明記されています。"
        }
      },
      "media_id": "local-U13",
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
      "text": "学校の行事で書かれた手紙なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.450930793012958,
      "judge_s": 2.8215079510118812,
      "luna_s": 2.8215079510118812,
      "total_s": 4.425399401050527,
      "writer_s": 1.6038914500386454
    }
  },
  {
    "case_id": "U13-e04",
    "record": {
      "comment_id": "U13-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 4282,
            "latency_s": 1.481622,
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
                "guess": 0.81,
                "question": 0.19
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.04,
                "point_1": 0.16
              },
              "C": 0.33,
              "D": {
                "irrelevant": 0.0,
                "no": 0.0,
                "yes": 1.0
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
            "completion_tokens": 166,
            "finish_reason": "stop",
            "latency_s": 2.77236,
            "model": "gpt-6-luna",
            "prompt_tokens": 2952,
            "reasoning_tokens": 107
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、後で読まれるよう意図して保管とあります。"
        }
      },
      "media_id": "local-U13",
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
      "text": "あとで読まれるように保管されてた？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.4819505809573457,
      "judge_s": 2.7724136309698224,
      "luna_s": 2.7724136309698224,
      "total_s": 4.100112491985783,
      "writer_s": 1.3276988610159606
    }
  },
  {
    "case_id": "U13-e05",
    "record": {
      "comment_id": "U13-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 4276,
            "latency_s": 1.545191,
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
                "point_0": 0.09,
                "point_1": 0.01
              },
              "C": 0.62,
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
            "completion_tokens": 189,
            "finish_reason": "stop",
            "latency_s": 2.81426,
            "model": "gpt-6-luna",
            "prompt_tokens": 2952,
            "reasoning_tokens": 117
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、男の子は男の息子ではないとされています。"
        }
      },
      "media_id": "local-U13",
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
      "text": "書いた男の子って、男の息子なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.5455371430143714,
      "judge_s": 2.814321607002057,
      "luna_s": 2.814321607002057,
      "total_s": 3.9735733779962175,
      "writer_s": 1.1592517709941603
    }
  },
  {
    "case_id": "U13-e06",
    "record": {
      "comment_id": "U13-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 7,
            "input_tokens": 4768,
            "latency_s": 1.626152,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 278,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.76,
                "question": 0.24
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A3": 0.79,
              "A_bare": 0.03,
              "B": {
                "point_0": 0.03,
                "point_1": 0.01
              },
              "C": 0.6,
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
            "completion_tokens": 210,
            "finish_reason": "stop",
            "latency_s": 3.015167,
            "model": "gpt-6-luna",
            "prompt_tokens": 2948,
            "reasoning_tokens": 145
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、その子は有名人ではないとされています。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。その子は有名人じゃないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "その子は有名人だったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.6264846039703116,
      "judge_s": 3.015220886969473,
      "luna_s": 3.015220886969473,
      "total_s": 5.552599378977902,
      "writer_s": 2.537378492008429
    }
  },
  {
    "case_id": "U13-e07",
    "record": {
      "comment_id": "U13-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 7,
            "input_tokens": 4789,
            "latency_s": 1.674237,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 278,
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
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A3": 0.88,
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02,
                "point_1": 0.01
              },
              "C": 0.84,
              "D": {
                "irrelevant": 0.0,
                "no": 0.94,
                "yes": 0.06
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
            "completion_tokens": 179,
            "finish_reason": "stop",
            "latency_s": 2.8478,
            "model": "gpt-6-luna",
            "prompt_tokens": 2950,
            "reasoning_tokens": 106
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "真相では、自分自身と会うことはできず、その子には一度も会っていません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。男はその子に会ったことがないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男はその子に会ったことがある？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.6745863480027765,
      "judge_s": 2.8478523349622265,
      "luna_s": 2.8478523349622265,
      "total_s": 5.163558962987736,
      "writer_s": 2.3157066280255094
    }
  },
  {
    "case_id": "U13-e08",
    "record": {
      "comment_id": "U13-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 4318,
            "latency_s": 1.45792,
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
                "guess": 0.56,
                "question": 0.44
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.02,
                "point_1": 0.02
              },
              "C": 0.64,
              "D": {
                "irrelevant": 0.01,
                "no": 0.99,
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
            "completion_tokens": 284,
            "finish_reason": "stop",
            "latency_s": 3.766784,
            "model": "gpt-6-luna",
            "prompt_tokens": 2958,
            "reasoning_tokens": 218
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "夢の内容は答えに関係しないと確定しています。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ほかのことも聞いてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "手紙に書かれてた夢の内容って、答えに関係ある？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.458467748016119,
      "judge_s": 3.766828029009048,
      "luna_s": 3.766828029009048,
      "total_s": 5.089998162002303,
      "writer_s": 1.3231701329932548
    }
  },
  {
    "case_id": "U13-e09",
    "record": {
      "comment_id": "U13-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 4270,
            "latency_s": 1.352488,
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
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.02,
                "point_1": 0.01
              },
              "C": 0.52,
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
            "completion_tokens": 253,
            "finish_reason": "stop",
            "latency_s": 3.322159,
            "model": "gpt-6-luna",
            "prompt_tokens": 2953,
            "reasoning_tokens": 176
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、手紙は宛先どおりの正しい受け取り手に渡ったとされています。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！宛先は男で合ってたよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "手紙の宛先は男で合ってたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.3527995509793982,
      "judge_s": 3.322219693043735,
      "luna_s": 3.322219693043735,
      "total_s": 5.913326747016981,
      "writer_s": 2.5911070539732464
    }
  },
  {
    "case_id": "U13-e10",
    "record": {
      "comment_id": "U13-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 4264,
            "latency_s": 1.650773,
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
                "guess": 0.16,
                "question": 0.84
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
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 252,
            "finish_reason": "stop",
            "latency_s": 3.581806,
            "model": "gpt-6-luna",
            "prompt_tokens": 2952,
            "reasoning_tokens": 186
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、受け取っても驚かず懐かしそうに笑ったとあります。"
        }
      },
      "media_id": "local-U13",
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
      "text": "男は手紙を読んで驚いてた？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.6510875019594096,
      "judge_s": 3.5818601910141297,
      "luna_s": 3.5818601910141297,
      "total_s": 4.543728584016208,
      "writer_s": 0.9618683930020779
    }
  },
  {
    "case_id": "U13-e11",
    "record": {
      "comment_id": "U13-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 2115,
            "latency_s": 1.058214,
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
                "guess": 0.01,
                "question": 0.99
              },
              "A2": {
                "q_multi": 0.94,
                "q_open": 0.06,
                "q_yesno": 0.0
              },
              "A_bare": 0.04
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
            "completion_tokens": 168,
            "finish_reason": "stop",
            "latency_s": 2.201733,
            "model": "gpt-6-luna",
            "prompt_tokens": 2953,
            "reasoning_tokens": 89
          },
          "error": null,
          "kind": "q_multi",
          "reason": "「いつ書いたか」と「誰が書いたか」の二つを尋ねているため。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつしてごらん。まずはどちらから聞こうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "手紙はいつ書いたの？誰が書いたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.0583405459765345,
      "judge_s": 2.2018290089908987,
      "luna_s": 2.2018290089908987,
      "total_s": 3.9238026129896753,
      "writer_s": 1.7219736039987765
    }
  },
  {
    "case_id": "U13-e12",
    "record": {
      "comment_id": "U13-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 2136,
            "latency_s": 0.603835,
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
                "guess": 0.0,
                "question": 1.0
              },
              "A2": {
                "q_multi": 0.99,
                "q_open": 0.01,
                "q_yesno": 0.0
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
            "completion_tokens": 146,
            "finish_reason": "stop",
            "latency_s": 2.101895,
            "model": "gpt-6-luna",
            "prompt_tokens": 2960,
            "reasoning_tokens": 67
          },
          "error": null,
          "kind": "q_multi",
          "reason": "受け取った場所と郵便で届いたかの質問が二つあります。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。まずはどちらか聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "どこで手紙を受け取ったの？それは郵便で届いたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.6040296530118212,
      "judge_s": 2.1019529729965143,
      "luna_s": 2.1019529729965143,
      "total_s": 9.88621178403264,
      "writer_s": 7.784258811036125
    }
  },
  {
    "case_id": "U13-e13",
    "record": {
      "comment_id": "U13-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "latency_s": 0.833285,
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
            "completion_tokens": 174,
            "finish_reason": "stop",
            "latency_s": 2.713104,
            "model": "gpt-6-luna",
            "prompt_tokens": 2959,
            "reasoning_tokens": 89
          },
          "error": null,
          "kind": "q_open",
          "reason": "「なぜ」と理由を尋ねる質問で、はい／いいえでは答えられません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "「男はその子のことを誰よりもよく知っていたの？」のように、はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "なぜ男は、その子がどんな子か誰よりよく知っていたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.833504903013818,
      "judge_s": 2.713168983987998,
      "luna_s": 2.713168983987998,
      "total_s": 7.544772337016184,
      "writer_s": 4.831603353028186
    }
  },
  {
    "case_id": "U13-e14",
    "record": {
      "comment_id": "U13-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 2652,
            "latency_s": 0.816652,
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
              "A3": 0.27,
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.27"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 223,
            "finish_reason": "stop",
            "latency_s": 3.179899,
            "model": "gpt-6-luna",
            "prompt_tokens": 2955,
            "reasoning_tokens": 137
          },
          "error": null,
          "kind": "q_open",
          "reason": "「どうして」は自由回答になるため、はい／いいえで答えられる質問ではありません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞いてごらん。「男はその子に会ったことがあるの？」のようにね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "どうして男はその子に一度も会っていないの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.8169300109730102,
      "judge_s": 3.179957612999715,
      "luna_s": 3.179957612999715,
      "total_s": 12.052210933004972,
      "writer_s": 8.872253320005257
    }
  },
  {
    "case_id": "U13-e15",
    "record": {
      "comment_id": "U13-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 7,
            "input_tokens": 4789,
            "latency_s": 2.026394,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 278,
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
              "A3": 0.74,
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02,
                "point_1": 0.01
              },
              "C": 0.68,
              "D": {
                "irrelevant": 0.01,
                "no": 0.86,
                "yes": 0.13
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
            "completion_tokens": 495,
            "finish_reason": "stop",
            "latency_s": 5.856652,
            "model": "gpt-6-luna",
            "prompt_tokens": 2950,
            "reasoning_tokens": 438
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "真相では、男はその子に一度も会っていません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ほかにはどんなことが気になるかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "その子は彼に会ったことがある？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 2.026794431032613,
      "judge_s": 5.856709301995579,
      "luna_s": 5.856709301995579,
      "total_s": 6.879992392030545,
      "writer_s": 1.0232830900349654
    }
  },
  {
    "case_id": "U13-e16",
    "record": {
      "comment_id": "U13-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 2267,
            "latency_s": 0.644554,
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
            "completion_tokens": 903,
            "finish_reason": "stop",
            "latency_s": 8.600692,
            "model": "gpt-6-luna",
            "prompt_tokens": 3009,
            "reasoning_tokens": 783
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "子どもの頃の自分がタイムカプセルに入れた手紙だと、核心をすべて説明しています。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！手紙は小学生の男が未来の自分へ書いたもの。50年後、同窓会でタイムカプセルから受け取った。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男が小学生のころ、未来の自分宛てに書いた手紙を学校のタイムカプセルに入れ、50年後の同窓会で受け取った。書いた子は昔の男自身だからよく知っているし、自分には会えなかったんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.644798164954409,
      "judge_s": 8.600752319965977,
      "luna_s": 8.600752319965977,
      "total_s": 8.600759905937593,
      "writer_s": 7.585971616208553e-06
    }
  },
  {
    "case_id": "U13-e17",
    "record": {
      "comment_id": "U13-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 2243,
            "latency_s": 0.638426,
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
                "point_0": 0.97,
                "point_1": 0.95
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
            "completion_tokens": 249,
            "finish_reason": "stop",
            "latency_s": 3.203355,
            "model": "gpt-6-luna",
            "prompt_tokens": 3001,
            "reasoning_tokens": 141
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "書き手が昔の自分であることと、タイムカプセルの仕掛けを両方言い当てています。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！手紙は小学生の男が未来の自分へ書いたもの。50年後、同窓会でタイムカプセルから受け取った。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "小学生の男が未来の自分に宛てて書いた手紙を、学校のタイムカプセルから同窓会で受け取った。書いた子は昔の自分だから、誰より知っていても会ったことはないってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.6386807640083134,
      "judge_s": 3.2035236670053564,
      "luna_s": 3.2035236670053564,
      "total_s": 3.2035259989788756,
      "writer_s": 2.3319735191762447e-06
    }
  },
  {
    "case_id": "U13-e18",
    "record": {
      "comment_id": "U13-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_wrong"
      },
      "judgements": {
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "guess_demoted": true,
            "input_tokens": 4390,
            "latency_s": 2.264611,
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
                "guess": 0.99,
                "question": 0.01
              },
              "A2": {
                "q_multi": 0.04,
                "q_open": 0.01,
                "q_yesno": 0.95
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.14,
                "point_1": 0.07
              },
              "C": 0.48,
              "D": {
                "irrelevant": 0.0,
                "no": 0.01,
                "yes": 0.99
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.07"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 315,
            "finish_reason": "stop",
            "latency_s": 4.640759,
            "model": "gpt-6-luna",
            "prompt_tokens": 2968,
            "reasoning_tokens": 245
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "保管や受け渡しには触れていますが、核心となる仕掛けの推理には至っていません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。別の考えも聞かせてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "学校で書かれた古い手紙が何十年も保管されていて、男に渡ったんじゃない？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 2.264916746993549,
      "judge_s": 4.640822365996428,
      "luna_s": 4.640822365996428,
      "total_s": 5.781597144028638,
      "writer_s": 1.1407747780322097
    }
  },
  {
    "case_id": "U13-e19",
    "record": {
      "comment_id": "U13-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 5,
            "guess_demoted": true,
            "input_tokens": 3201,
            "latency_s": 1.127766,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 218,
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
                "q_multi": 0.26,
                "q_open": 0.02,
                "q_yesno": 0.72
              },
              "A3": 0.21,
              "A_bare": 0.03,
              "B": {
                "point_0": 0.09,
                "point_1": 0.03
              }
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 要点最低=0.03"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 1089,
            "finish_reason": "stop",
            "latency_s": 11.404371,
            "model": "gpt-6-luna",
            "prompt_tokens": 2967,
            "reasoning_tokens": 1017
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "未来の宛先には触れていますが、仕掛けの核心は述べられていません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "手紙は未来の誰かに宛てたもので、男はその子についてよく知っていたのかな。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.1281019369489513,
      "judge_s": 11.404427886009216,
      "luna_s": 11.404427886009216,
      "total_s": 13.193112095003016,
      "writer_s": 1.7886842089938
    }
  },
  {
    "case_id": "U13-e20",
    "record": {
      "comment_id": "U13-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 2624,
            "latency_s": 0.903194,
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
                "q_open": 0.83,
                "q_yesno": 0.16
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.05,
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
            "completion_tokens": 218,
            "finish_reason": "stop",
            "latency_s": 3.331782,
            "model": "gpt-6-luna",
            "prompt_tokens": 2962,
            "reasoning_tokens": 155
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "配達遅延という推測で、核心の仕掛けには触れていません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。別の考え方もしてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "郵便局が配達を忘れていて、50年後に遅れて届けたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.9034796869964339,
      "judge_s": 3.3318396570393816,
      "luna_s": 3.3318396570393816,
      "total_s": 4.559835778083652,
      "writer_s": 1.2279961210442707
    }
  },
  {
    "case_id": "U13-e21",
    "record": {
      "comment_id": "U13-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 2656,
            "latency_s": 0.886604,
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
                "q_multi": 0.05,
                "q_open": 0.6,
                "q_yesno": 0.35
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.07,
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
            "completion_tokens": 285,
            "finish_reason": "stop",
            "latency_s": 3.806922,
            "model": "gpt-6-luna",
            "prompt_tokens": 2968,
            "reasoning_tokens": 222
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "手紙を書いた人物について推理していますが、核心の要点には触れていません。"
        }
      },
      "media_id": "local-U13",
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
      "shadow_mismatch": false,
      "text": "手紙を書いたのは男の息子で、男はその子のことを周りから聞いて知ったんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.8871963450219482,
      "judge_s": 3.806951617996674,
      "luna_s": 3.806951617996674,
      "total_s": 7.478065406961832,
      "writer_s": 3.671113788965158
    }
  },
  {
    "case_id": "U13-b22",
    "record": {
      "comment_id": "U13-b22",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 4246,
            "latency_s": 1.170375,
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
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.02,
                "point_1": 0.01
              },
              "C": 0.39,
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
            "completion_tokens": 209,
            "finish_reason": "stop",
            "latency_s": 3.385635,
            "model": "gpt-6-luna",
            "prompt_tokens": 2949,
            "reasoning_tokens": 150
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "手紙は郵便ではなく、集まりの場で男に手渡されています。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。郵便で届いたわけじゃないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "手紙は郵便で届いたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.1706676589674316,
      "judge_s": 3.3856956280069426,
      "luna_s": 3.3856956280069426,
      "total_s": 7.920944686047733,
      "writer_s": 4.53524905804079
    }
  },
  {
    "case_id": "U13-b23",
    "record": {
      "comment_id": "U13-b23",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 7,
            "input_tokens": 4761,
            "latency_s": 1.62473,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 278,
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
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A3": 0.8,
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01,
                "point_1": 0.01
              },
              "C": 0.59,
              "D": {
                "irrelevant": 0.02,
                "no": 0.97,
                "yes": 0.01
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
            "completion_tokens": 162,
            "finish_reason": "stop",
            "latency_s": 2.950325,
            "model": "gpt-6-luna",
            "prompt_tokens": 2948,
            "reasoning_tokens": 95
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "男の子は男の息子ではないと確定しています。"
        }
      },
      "media_id": "local-U13",
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
      "text": "男はその子の父親なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.625089013017714,
      "judge_s": 2.9503795169875957,
      "luna_s": 2.9503795169875957,
      "total_s": 6.3251399919972755,
      "writer_s": 3.37476047500968
    }
  },
  {
    "case_id": "U13-b24",
    "record": {
      "comment_id": "U13-b24",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 7,
            "input_tokens": 4796,
            "latency_s": 1.542228,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 278,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.88,
                "question": 0.12
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A3": 0.71,
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02,
                "point_1": 0.01
              },
              "C": 0.44,
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
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 361,
            "finish_reason": "stop",
            "latency_s": 4.977482,
            "model": "gpt-6-luna",
            "prompt_tokens": 2952,
            "reasoning_tokens": 286
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "はい・いいえで答えられる質問で、仕事を通じて知った事実はありません。"
        }
      },
      "media_id": "local-U13",
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
      "text": "仕事を通じてその子を知ってたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.542570676014293,
      "judge_s": 4.9775330609991215,
      "luna_s": 4.9775330609991215,
      "total_s": 6.053993868001271,
      "writer_s": 1.0764608070021495
    }
  },
  {
    "case_id": "U13-b25",
    "record": {
      "comment_id": "U13-b25",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": "yes",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "unknown",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4258,
            "latency_s": 1.244946,
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
                "guess": 0.64,
                "question": 0.36
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.01,
                "q_yesno": 0.98
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.03,
                "point_1": 0.02
              },
              "C": 0.47,
              "D": {
                "irrelevant": 0.03,
                "no": 0.51,
                "yes": 0.46
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
            "completion_tokens": 891,
            "finish_reason": "stop",
            "latency_s": 9.821682,
            "model": "gpt-6-luna",
            "prompt_tokens": 2950,
            "reasoning_tokens": 804
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "男は自分の子ども時代を知っていたため、手紙が届く前から知っていたと判断できます。"
        }
      },
      "media_id": "local-U13",
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
      "shadow_mismatch": true,
      "text": "手紙が届く前から知ってた？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.2452131710015237,
      "judge_s": 9.821735153032932,
      "luna_s": 9.821735153032932,
      "total_s": 10.693015219061635,
      "writer_s": 0.871280066028703
    }
  },
  {
    "case_id": "U13-b26",
    "record": {
      "comment_id": "U13-b26",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 7,
            "input_tokens": 4768,
            "latency_s": 1.446569,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 278,
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
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A3": 0.75,
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01,
                "point_1": 0.01
              },
              "C": 0.56,
              "D": {
                "irrelevant": 0.2,
                "no": 0.8,
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
            "completion_tokens": 388,
            "finish_reason": "stop",
            "latency_s": 5.329386,
            "model": "gpt-6-luna",
            "prompt_tokens": 2949,
            "reasoning_tokens": 319
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "主治医かどうかは、問題の核心とは関係ありません。"
        }
      },
      "media_id": "local-U13",
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
      "shadow_mismatch": true,
      "text": "男はその子の主治医なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.447086728992872,
      "judge_s": 5.329441245005,
      "luna_s": 5.329441245005,
      "total_s": 6.543119520007167,
      "writer_s": 1.2136782750021666
    }
  },
  {
    "case_id": "U13-b27",
    "record": {
      "comment_id": "U13-b27",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 7,
            "input_tokens": 4768,
            "latency_s": 1.762263,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 278,
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
              "A3": 0.75,
              "A_bare": 0.03,
              "B": {
                "point_0": 0.04,
                "point_1": 0.01
              },
              "C": 0.48,
              "D": {
                "irrelevant": 0.01,
                "no": 0.15,
                "yes": 0.84
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
            "completion_tokens": 276,
            "finish_reason": "stop",
            "latency_s": 4.353601,
            "model": "gpt-6-luna",
            "prompt_tokens": 2948,
            "reasoning_tokens": 206
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "質問の対象は手紙を書いた男の子で、真相から実在すると分かります。"
        }
      },
      "media_id": "local-U13",
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
      "text": "その子は実在する子なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.7626421190216206,
      "judge_s": 4.353635372011922,
      "luna_s": 4.353635372011922,
      "total_s": 6.070080525008962,
      "writer_s": 1.7164451529970393
    }
  },
  {
    "case_id": "U13-b28",
    "record": {
      "comment_id": "U13-b28",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 4228,
            "latency_s": 1.301542,
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
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.04,
              "B": {
                "point_0": 0.01,
                "point_1": 0.01
              },
              "C": 0.51,
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
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "completion_tokens": 155,
            "finish_reason": "stop",
            "latency_s": 3.048632,
            "model": "gpt-6-luna",
            "prompt_tokens": 2946,
            "reasoning_tokens": 80
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "男が有名人かどうかは、手紙の仕掛けや真相に関係しません。"
        }
      },
      "media_id": "local-U13",
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
      "shadow_mismatch": true,
      "text": "男は有名人なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.3018136529717594,
      "judge_s": 3.048688137962017,
      "luna_s": 3.048688137962017,
      "total_s": 4.219170046970248,
      "writer_s": 1.170481909008231
    }
  },
  {
    "case_id": "U13-t01",
    "record": {
      "comment_id": "U13-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "タイムカプセル",
          "debug": {
            "calls": 1,
            "input_tokens": 931,
            "latency_s": 0.186857,
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
          "bare_term": "タイムカプセル",
          "debug": {
            "completion_tokens": 175,
            "finish_reason": "stop",
            "latency_s": 2.561901,
            "model": "gpt-6-luna",
            "prompt_tokens": 2944,
            "reasoning_tokens": 89
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句だけのコメントなので、質問として聞き直しを促します。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "タイムカプセルが何のことか、もう少し詳しく教えて！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "タイムカプセル",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.18695583898806944,
      "judge_s": 2.561957350000739,
      "luna_s": 2.561957350000739,
      "total_s": 6.019658953999169,
      "writer_s": 3.45770160399843
    }
  },
  {
    "case_id": "U13-t02",
    "record": {
      "comment_id": "U13-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "同窓会",
          "debug": {
            "calls": 1,
            "input_tokens": 929,
            "latency_s": 0.189341,
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
              "A_bare": 0.91
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.91"
        },
        "luna": {
          "answer": null,
          "bare_term": "同窓会",
          "debug": {
            "completion_tokens": 142,
            "finish_reason": "stop",
            "latency_s": 2.260968,
            "model": "gpt-6-luna",
            "prompt_tokens": 2944,
            "reasoning_tokens": 71
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句のみのコメントなので、q_openです。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "同窓会が何のことか、もう少し詳しく教えて！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "同窓会？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.18944920197827742,
      "judge_s": 2.261027845030185,
      "luna_s": 2.261027845030185,
      "total_s": 5.906000438029878,
      "writer_s": 3.644972592999693
    }
  },
  {
    "case_id": "U13-t03",
    "record": {
      "comment_id": "U13-t03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "手紙",
          "debug": {
            "calls": 1,
            "input_tokens": 927,
            "latency_s": 0.210902,
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
              "A_bare": 0.93
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.93"
        },
        "luna": {
          "answer": null,
          "bare_term": "手紙",
          "debug": {
            "completion_tokens": 164,
            "finish_reason": "stop",
            "latency_s": 2.584273,
            "model": "gpt-6-luna",
            "prompt_tokens": 2942,
            "reasoning_tokens": 89
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない名詞だけのコメントなので、質問として一意に答えられません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "手紙がどうしたのか聞かせてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "手紙？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.21098880103090778,
      "judge_s": 2.584299391019158,
      "luna_s": 2.584299391019158,
      "total_s": 5.348540339036845,
      "writer_s": 2.7642409480176866
    }
  },
  {
    "case_id": "c-ask_hint-02",
    "record": {
      "comment_id": "c-ask_hint-02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "ask_hint"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1431,
            "latency_s": 0.404879,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 122,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.0,
                "request": 1.0
              },
              "A2": {
                "ask_hint": 1.0,
                "ask_howto": 0.0,
                "ask_spoiler": 0.0
              },
              "A_bare": 0.24
            }
          },
          "error": null,
          "kind": "ask_hint",
          "reason": "段A=request→ask_hint"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 185,
            "finish_reason": "stop",
            "latency_s": 3.042435,
            "model": "gpt-6-luna",
            "prompt_tokens": 2948,
            "reasoning_tokens": 108
          },
          "error": null,
          "kind": "ask_hint",
          "reason": "ヒントを求めているため、質問で絞るよう促します。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ヒントは出せないんだ。質問で少しずつ絞っていこうね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "ちょっとだけヒントほしい〜",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.40499788901070133,
      "judge_s": 3.04249326500576,
      "luna_s": 3.04249326500576,
      "total_s": 7.2993682870292105,
      "writer_s": 4.256875022023451
    }
  },
  {
    "case_id": "c-ask_hint-04",
    "record": {
      "comment_id": "c-ask_hint-04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "ask_hint"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1427,
            "latency_s": 0.37903,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 122,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.01,
                "reaction": 0.24,
                "request": 0.75
              },
              "A2": {
                "ask_hint": 0.7,
                "ask_howto": 0.02,
                "ask_spoiler": 0.28
              },
              "A_bare": 0.19
            }
          },
          "error": null,
          "kind": "ask_hint",
          "reason": "段A=request→ask_hint"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 244,
            "finish_reason": "stop",
            "latency_s": 3.396509,
            "model": "gpt-6-luna",
            "prompt_tokens": 2948,
            "reasoning_tokens": 164
          },
          "error": null,
          "kind": "ask_hint",
          "reason": "解答に詰まり、助けを求めているためヒント要求と判断。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ヒントは出せないけど、質問で少しずつ絞っていこう。はい・いいえで答えられる質問をしてごらん☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "詰まった、助けて🙏",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.379138198972214,
      "judge_s": 3.396558137028478,
      "luna_s": 3.396558137028478,
      "total_s": 7.980554005072918,
      "writer_s": 4.58399586804444
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
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "latency_s": 0.507975,
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
            "completion_tokens": 177,
            "finish_reason": "stop",
            "latency_s": 3.333687,
            "model": "gpt-6-luna",
            "prompt_tokens": 2945,
            "reasoning_tokens": 94
          },
          "error": null,
          "kind": "ask_spoiler",
          "reason": "答えだけを求めているため、ネタバレ希望と判断しました。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問には答えられるけど、真相は教えられないよ。質問で少しずつ絞っていこう☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "答えだけ教えて〜",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.5080977610195987,
      "judge_s": 3.33373545500217,
      "luna_s": 3.33373545500217,
      "total_s": 5.6299524520291016,
      "writer_s": 2.2962169970269315
    }
  },
  {
    "case_id": "c-ask_spoiler-03",
    "record": {
      "comment_id": "c-ask_spoiler-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1427,
            "latency_s": 0.434755,
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
              "A_bare": 0.05
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
            "completion_tokens": 163,
            "finish_reason": "stop",
            "latency_s": 2.405184,
            "model": "gpt-6-luna",
            "prompt_tokens": 2947,
            "reasoning_tokens": 85
          },
          "error": null,
          "kind": "ask_spoiler",
          "reason": "真相を直接教えてほしいという依頼です。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問には答えられるけど、真相は教えられないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "もう真相言っちゃって！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.4348689860198647,
      "judge_s": 2.405209464021027,
      "luna_s": 2.405209464021027,
      "total_s": 6.126869153988082,
      "writer_s": 3.721659689967055
    }
  },
  {
    "case_id": "c-ask_spoiler-05",
    "record": {
      "comment_id": "c-ask_spoiler-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1417,
            "latency_s": 0.401733,
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
                "ask_howto": 0.0,
                "ask_spoiler": 1.0
              },
              "A_bare": 0.43
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
            "completion_tokens": 241,
            "finish_reason": "stop",
            "latency_s": 2.986952,
            "model": "gpt-6-luna",
            "prompt_tokens": 2944,
            "reasoning_tokens": 159
          },
          "error": null,
          "kind": "ask_spoiler",
          "reason": "答えの解説を求めるコメントのため、ネタバレ要求と判定。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問には答えられるけど、真相は教えられないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "解説まだー？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.4018784660147503,
      "judge_s": 2.9869725430035032,
      "luna_s": 2.9869725430035032,
      "total_s": 4.260541572002694,
      "writer_s": 1.2735690289991908
    }
  },
  {
    "case_id": "c-ask_howto-02",
    "record": {
      "comment_id": "c-ask_howto-02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "latency_s": 0.383903,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 124,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.05,
                "reaction": 0.0,
                "request": 0.95
              },
              "A2": {
                "ask_hint": 0.0,
                "ask_howto": 1.0,
                "ask_spoiler": 0.0
              },
              "A_bare": 0.05
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
            "completion_tokens": 171,
            "finish_reason": "stop",
            "latency_s": 2.452545,
            "model": "gpt-6-luna",
            "prompt_tokens": 2947,
            "reasoning_tokens": 87
          },
          "error": null,
          "kind": "ask_howto",
          "reason": "コメントの仕方を尋ねているため、遊び方の案内に該当します。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる質問をコメントしてごらん。私が答えるよ！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "何をコメントしたらいいの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.384155631007161,
      "judge_s": 2.4526335350237787,
      "luna_s": 2.4526335350237787,
      "total_s": 4.802933631988708,
      "writer_s": 2.3503000969649293
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
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "latency_s": 0.425673,
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
            "completion_tokens": 252,
            "finish_reason": "stop",
            "latency_s": 3.007067,
            "model": "gpt-6-luna",
            "prompt_tokens": 2949,
            "reasoning_tokens": 173
          },
          "error": null,
          "kind": "ask_howto",
          "reason": "質問への返答方法を尋ねる、遊び方についての質問です。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる質問をコメントしてごらん。私が答えるよ！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "質問したら返事もらえるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.42584062897367403,
      "judge_s": 3.0071140530053526,
      "luna_s": 3.0071140530053526,
      "total_s": 4.253744319954421,
      "writer_s": 1.2466302669490688
    }
  },
  {
    "case_id": "c-impression-01",
    "record": {
      "comment_id": "c-impression-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "latency_s": 0.438553,
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
                "chat": 0.03,
                "cheer": 0.43,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.54,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.07
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
            "completion_tokens": 113,
            "finish_reason": "stop",
            "latency_s": 2.220588,
            "model": "gpt-6-luna",
            "prompt_tokens": 2943,
            "reasoning_tokens": 56
          },
          "error": null,
          "kind": "impression",
          "reason": "シリーズへの好意を伝える感想コメントです。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ありがとう！楽しんでくれてうれしいよ☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "このシリーズ好き！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.4387417300022207,
      "judge_s": 2.2206514239660464,
      "luna_s": 2.2206514239660464,
      "total_s": 5.963619911985006,
      "writer_s": 3.7429684880189598
    }
  },
  {
    "case_id": "c-impression-03",
    "record": {
      "comment_id": "c-impression-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1594,
            "latency_s": 0.389771,
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
              "A_bare": 0.04
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
            "completion_tokens": 181,
            "finish_reason": "stop",
            "latency_s": 3.056825,
            "model": "gpt-6-luna",
            "prompt_tokens": 2949,
            "reasoning_tokens": 117
          },
          "error": null,
          "kind": "impression",
          "reason": "問題の雰囲気への感想を述べているため。"
        }
      },
      "media_id": "local-U13",
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
      "text": "今回の設定ちょっと怖くて好き",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.3899008990265429,
      "judge_s": 3.05688976298552,
      "luna_s": 3.05688976298552,
      "total_s": 4.52318528899923,
      "writer_s": 1.4662955260137096
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
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "latency_s": 0.468295,
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
              "A_bare": 0.09
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
            "completion_tokens": 158,
            "finish_reason": "stop",
            "latency_s": 2.576535,
            "model": "gpt-6-luna",
            "prompt_tokens": 2948,
            "reasoning_tokens": 94
          },
          "error": null,
          "kind": "impression",
          "reason": "問題の短さと奥深さを評価する感想です。"
        }
      },
      "media_id": "local-U13",
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
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.4684387070010416,
      "judge_s": 2.5766081269830465,
      "luna_s": 2.5766081269830465,
      "total_s": 5.966088064014912,
      "writer_s": 3.389479937031865
    }
  },
  {
    "case_id": "c-greeting-02",
    "record": {
      "comment_id": "c-greeting-02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1578,
            "latency_s": 0.413242,
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
              "A_bare": 0.37
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
            "completion_tokens": 134,
            "finish_reason": "stop",
            "latency_s": 2.283339,
            "model": "gpt-6-luna",
            "prompt_tokens": 2941,
            "reasoning_tokens": 80
          },
          "error": null,
          "kind": "greeting",
          "reason": "挨拶のみのコメントです。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "こんばんは！来てくれてうれしいよ☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "こんばんは！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.4133926709764637,
      "judge_s": 2.283361902984325,
      "luna_s": 2.283361902984325,
      "total_s": 3.5197141639655456,
      "writer_s": 1.2363522609812208
    }
  },
  {
    "case_id": "c-greeting-04",
    "record": {
      "comment_id": "c-greeting-04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1574,
            "latency_s": 0.383227,
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
                "chat": 0.01,
                "cheer": 0.0,
                "complaint": 0.0,
                "greeting": 0.99,
                "impression": 0.0,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.59
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
            "completion_tokens": 140,
            "finish_reason": "stop",
            "latency_s": 2.553198,
            "model": "gpt-6-luna",
            "prompt_tokens": 2943,
            "reasoning_tokens": 86
          },
          "error": null,
          "kind": "greeting",
          "reason": "挨拶への返答です。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "やっほー！来てくれてうれしいよ☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "やっほー",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.38336189702386037,
      "judge_s": 2.5532730050035752,
      "luna_s": 2.5532730050035752,
      "total_s": 3.812403538962826,
      "writer_s": 1.259130533959251
    }
  },
  {
    "case_id": "c-cheer-01",
    "record": {
      "comment_id": "c-cheer-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1590,
            "latency_s": 0.472339,
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
                "chat": 0.01,
                "cheer": 0.86,
                "complaint": 0.0,
                "greeting": 0.13,
                "impression": 0.0,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.1
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
            "completion_tokens": 127,
            "finish_reason": "stop",
            "latency_s": 2.278165,
            "model": "gpt-6-luna",
            "prompt_tokens": 2949,
            "reasoning_tokens": 70
          },
          "error": null,
          "kind": "cheer",
          "reason": "投稿へのねぎらいと応援のコメントです。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ありがとう！うれしいな☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "今日も投稿おつかれさま！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.47249193297466263,
      "judge_s": 2.2782278140075505,
      "luna_s": 2.2782278140075505,
      "total_s": 3.7367806649999693,
      "writer_s": 1.4585528509924188
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
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "latency_s": 0.437071,
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
                "chat": 0.01,
                "cheer": 0.93,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.02,
                "mention": 0.0,
                "request": 0.04
              },
              "A_bare": 0.06
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
            "completion_tokens": 144,
            "finish_reason": "stop",
            "latency_s": 3.001268,
            "model": "gpt-6-luna",
            "prompt_tokens": 2947,
            "reasoning_tokens": 89
          },
          "error": null,
          "kind": "cheer",
          "reason": "更新を楽しみにしている応援コメントです。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ありがとう〜！楽しみにしててね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "更新たのしみにしてる〜",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.43738070398103446,
      "judge_s": 3.0013270640047267,
      "luna_s": 3.0013270640047267,
      "total_s": 6.224961032043211,
      "writer_s": 3.2236339680384845
    }
  },
  {
    "case_id": "c-cheer-05",
    "record": {
      "comment_id": "c-cheer-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1602,
            "latency_s": 0.460085,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 149,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.98,
                "request": 0.02
              },
              "A2": {
                "chat": 0.0,
                "cheer": 0.99,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.0,
                "mention": 0.0,
                "request": 0.01
              },
              "A_bare": 0.04
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
            "completion_tokens": 254,
            "finish_reason": "stop",
            "latency_s": 3.369653,
            "model": "gpt-6-luna",
            "prompt_tokens": 2951,
            "reasoning_tokens": 188
          },
          "error": null,
          "kind": "cheer",
          "reason": "アカウントへの好意を示し、継続を願う応援コメントです。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ありがとう！これからもよろしくね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "このアカウント好きだから続けてほしい",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.46023836196400225,
      "judge_s": 3.3697306370013393,
      "luna_s": 3.3697306370013393,
      "total_s": 11.37258414097596,
      "writer_s": 8.00285350397462
    }
  },
  {
    "case_id": "c-chat-02",
    "record": {
      "comment_id": "c-chat-02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1582,
            "latency_s": 0.427614,
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
                "chat": 1.0,
                "cheer": 0.0,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.0,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.07
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
            "completion_tokens": 210,
            "finish_reason": "stop",
            "latency_s": 3.193342,
            "model": "gpt-6-luna",
            "prompt_tokens": 2946,
            "reasoning_tokens": 150
          },
          "error": null,
          "kind": "chat",
          "reason": "問題への感想ではなく、見ている状況についての雑談です。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "通勤中に見てくれてありがとう☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "通勤中に見てます",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.4277887669741176,
      "judge_s": 3.1933947130455635,
      "luna_s": 3.1933947130455635,
      "total_s": 4.587726799072698,
      "writer_s": 1.3943320860271342
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
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "latency_s": 0.371229,
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
            "completion_tokens": 178,
            "finish_reason": "stop",
            "latency_s": 4.166571,
            "model": "gpt-6-luna",
            "prompt_tokens": 2949,
            "reasoning_tokens": 112
          },
          "error": null,
          "kind": "chat",
          "reason": "問題とは関係のない、週末の過ぎる早さについての雑談です。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ほんと、あっという間だね〜☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "週末ってあっという間だなー",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.37144582596374676,
      "judge_s": 4.166651086998172,
      "luna_s": 4.166651086998172,
      "total_s": 5.881776642985642,
      "writer_s": 1.7151255559874699
    }
  },
  {
    "case_id": "c-request-01",
    "record": {
      "comment_id": "c-request-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1596,
            "latency_s": 0.410236,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 148,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.98,
                "request": 0.02
              },
              "A2": {
                "chat": 0.0,
                "cheer": 0.0,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.0,
                "mention": 0.0,
                "request": 1.0
              },
              "A_bare": 0.11
            }
          },
          "error": null,
          "kind": "request",
          "reason": "段A=reaction→request"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 119,
            "finish_reason": "stop",
            "latency_s": 2.249484,
            "model": "gpt-6-luna",
            "prompt_tokens": 2951,
            "reasoning_tokens": 62
          },
          "error": null,
          "kind": "request",
          "reason": "次に出す問題のテーマをリクエストしているため。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "リクエストありがとう、うれしいな！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "次は学校が舞台の問題が見たい！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.41040429595159367,
      "judge_s": 2.2495387000381015,
      "luna_s": 2.2495387000381015,
      "total_s": 4.774223504064139,
      "writer_s": 2.5246848040260375
    }
  },
  {
    "case_id": "c-request-03",
    "record": {
      "comment_id": "c-request-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1590,
            "latency_s": 0.419251,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 148,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.74,
                "request": 0.26
              },
              "A2": {
                "chat": 0.0,
                "cheer": 0.0,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.0,
                "mention": 0.0,
                "request": 1.0
              },
              "A_bare": 0.14
            }
          },
          "error": null,
          "kind": "request",
          "reason": "段A=reaction→request"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 128,
            "finish_reason": "stop",
            "latency_s": 2.401782,
            "model": "gpt-6-luna",
            "prompt_tokens": 2945,
            "reasoning_tokens": 71
          },
          "error": null,
          "kind": "request",
          "reason": "怖めの問題を出してほしいというリクエストです。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "リクエストありがとう！覚えておくね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "怖めの問題もお願いします",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.4194396879756823,
      "judge_s": 2.4018286270438693,
      "luna_s": 2.4018286270438693,
      "total_s": 6.481326435052324,
      "writer_s": 4.079497808008455
    }
  },
  {
    "case_id": "c-request-05",
    "record": {
      "comment_id": "c-request-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1592,
            "latency_s": 0.447412,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 148,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.97,
                "request": 0.03
              },
              "A2": {
                "chat": 0.0,
                "cheer": 0.0,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.0,
                "mention": 0.0,
                "request": 1.0
              },
              "A_bare": 0.07
            }
          },
          "error": null,
          "kind": "request",
          "reason": "段A=reaction→request"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 108,
            "finish_reason": "stop",
            "latency_s": 2.840524,
            "model": "gpt-6-luna",
            "prompt_tokens": 2949,
            "reasoning_tokens": 49
          },
          "error": null,
          "kind": "request",
          "reason": "次に出してほしい問題のテーマを希望するリクエストです。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "リクエストありがとう！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "次は家族もの出してほしいな",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.44760286901146173,
      "judge_s": 2.8405757560394704,
      "luna_s": 2.8405757560394704,
      "total_s": 4.808671223989222,
      "writer_s": 1.9680954679497518
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
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "latency_s": 0.419203,
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
                "chat": 0.01,
                "cheer": 0.0,
                "complaint": 0.61,
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
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 176,
            "finish_reason": "stop",
            "latency_s": 2.63351,
            "model": "gpt-6-luna",
            "prompt_tokens": 2951,
            "reasoning_tokens": 117
          },
          "error": null,
          "kind": "complaint",
          "reason": "前の投稿との設定の重複を指摘しているため"
        }
      },
      "media_id": "local-U13",
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
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.4194167489768006,
      "judge_s": 2.633538544003386,
      "luna_s": 2.633538544003386,
      "total_s": 4.00297471502563,
      "writer_s": 1.3694361710222438
    }
  },
  {
    "case_id": "c-complaint-04",
    "record": {
      "comment_id": "c-complaint-04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1596,
            "latency_s": 0.400937,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 149,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.05,
                "reaction": 0.95,
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
              "A_bare": 0.06
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
            "completion_tokens": 130,
            "finish_reason": "stop",
            "latency_s": 2.178734,
            "model": "gpt-6-luna",
            "prompt_tokens": 2949,
            "reasoning_tokens": 65
          },
          "error": null,
          "kind": "complaint",
          "reason": "問題文に矛盾があるという指摘のため、クレームに分類します。"
        }
      },
      "media_id": "local-U13",
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
      "shadow_mismatch": false,
      "text": "問題文に矛盾があると思います",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.4011106980033219,
      "judge_s": 2.1787986169802025,
      "luna_s": 2.1787986169802025,
      "total_s": 10.190632837940939,
      "writer_s": 8.011834220960736
    }
  },
  {
    "case_id": "c-mention-01",
    "record": {
      "comment_id": "c-mention-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1588,
            "latency_s": 1.602125,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 148,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.99,
                "request": 0.01
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
              "A_bare": 0.04
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
            "completion_tokens": 134,
            "finish_reason": "stop",
            "latency_s": 2.222108,
            "model": "gpt-6-luna",
            "prompt_tokens": 2949,
            "reasoning_tokens": 69
          },
          "error": null,
          "kind": "mention",
          "reason": "友達をタグ付けして一緒に解こうと呼びかけているため"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいね、一緒に考えよう！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "@mika これ一緒に解こ！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 1.6022959370166063,
      "judge_s": 2.2221648789709434,
      "luna_s": 2.2221648789709434,
      "total_s": 5.917707442946266,
      "writer_s": 3.695542563975323
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
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "latency_s": 0.496907,
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
            "completion_tokens": 136,
            "finish_reason": "stop",
            "latency_s": 2.946437,
            "model": "gpt-6-luna",
            "prompt_tokens": 2947,
            "reasoning_tokens": 76
          },
          "error": null,
          "kind": "mention",
          "reason": "友達をタグ付けして問題を勧めているため。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "タグ付けありがとう、うれしいよ☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "@yuki こういうの好きそう",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.4970195650239475,
      "judge_s": 2.946493258990813,
      "luna_s": 2.946493258990813,
      "total_s": 5.378806768043432,
      "writer_s": 2.4323135090526193
    }
  },
  {
    "case_id": "c-mention-05",
    "record": {
      "comment_id": "c-mention-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "latency_s": 0.486713,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 148,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.02,
                "reaction": 0.93,
                "request": 0.04
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
              "A_bare": 0.06
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
            "completion_tokens": 113,
            "finish_reason": "stop",
            "latency_s": 3.026496,
            "model": "gpt-6-luna",
            "prompt_tokens": 2949,
            "reasoning_tokens": 50
          },
          "error": null,
          "kind": "mention",
          "reason": "友達にメンションし、あとで考えるよう促しているコメントです。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "うん、ゆっくり考えてみてね！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "@hana あとで考えてみて！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.48688499396666884,
      "judge_s": 3.026541417988483,
      "luna_s": 3.026541417988483,
      "total_s": 7.646793192951009,
      "writer_s": 4.620251774962526
    }
  },
  {
    "case_id": "c-emoji_only-02",
    "record": {
      "comment_id": "c-emoji_only-02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "completion_tokens": 91,
            "finish_reason": "stop",
            "latency_s": 1.97605,
            "model": "gpt-6-luna",
            "prompt_tokens": 2941,
            "reasoning_tokens": 37
          },
          "error": null,
          "kind": "emoji_only",
          "reason": "絵文字のみのコメントなので、emoji_onlyに分類します。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ありがとう、うれしいよ☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "😂👏",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 2.4544016923755407e-05,
      "judge_s": 1.9761288050212897,
      "luna_s": 1.9761288050212897,
      "total_s": 3.167281456058845,
      "writer_s": 1.1911526510375552
    }
  },
  {
    "case_id": "c-emoji_only-04",
    "record": {
      "comment_id": "c-emoji_only-04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "completion_tokens": 121,
            "finish_reason": "stop",
            "latency_s": 2.290175,
            "model": "gpt-6-luna",
            "prompt_tokens": 2941,
            "reasoning_tokens": 64
          },
          "error": null,
          "kind": "emoji_only",
          "reason": "絵文字だけで構成されたコメントのため、emoji_onlyに分類します。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ありがとう、うれしいよ☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "👍✨",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 3.754999488592148e-05,
      "judge_s": 2.2902104050153866,
      "luna_s": 2.2902104050153866,
      "total_s": 4.79321139404783,
      "writer_s": 2.5030009890324436
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
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "latency_s": 0.415273,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
            "probabilities": {
              "A1": {
                "inappropriate": 0.85,
                "other": 0.0,
                "question_or_guess": 0.02,
                "reaction": 0.13,
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
            "completion_tokens": 92,
            "finish_reason": "stop",
            "latency_s": 2.686904,
            "model": "gpt-6-luna",
            "prompt_tokens": 2949,
            "reasoning_tokens": 45
          },
          "error": null,
          "kind": "troll",
          "reason": "意味の取れない文字列の連続です。"
        }
      },
      "media_id": "local-U13",
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
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.41540653904667124,
      "judge_s": 2.686963326006662,
      "luna_s": 2.686963326006662,
      "total_s": 2.6869927080115303,
      "writer_s": 2.9382004868239164e-05
    }
  },
  {
    "case_id": "c-troll-03",
    "record": {
      "comment_id": "c-troll-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1468,
            "latency_s": 0.376103,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
            "probabilities": {
              "A1": {
                "inappropriate": 0.96,
                "other": 0.0,
                "question_or_guess": 0.01,
                "reaction": 0.03,
                "request": 0.0
              },
              "A2": {
                "abuse": 0.0,
                "personal_info": 0.0,
                "spam": 0.0,
                "troll": 1.0
              },
              "A_bare": 0.31
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
            "completion_tokens": 126,
            "finish_reason": "stop",
            "latency_s": 2.587867,
            "model": "gpt-6-luna",
            "prompt_tokens": 2947,
            "reasoning_tokens": 70
          },
          "error": null,
          "kind": "troll",
          "reason": "意味の取れない文字列の連続で、問題への推理や質問ではありません。"
        }
      },
      "media_id": "local-U13",
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
      "text": "らららららららら",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.37625328300055116,
      "judge_s": 2.5879489820217714,
      "luna_s": 2.5879489820217714,
      "total_s": 2.587954784044996,
      "writer_s": 5.802023224532604e-06
    }
  },
  {
    "case_id": "c-troll-05",
    "record": {
      "comment_id": "c-troll-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1466,
            "latency_s": 0.379245,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
            "probabilities": {
              "A1": {
                "inappropriate": 0.93,
                "other": 0.0,
                "question_or_guess": 0.04,
                "reaction": 0.03,
                "request": 0.0
              },
              "A2": {
                "abuse": 0.0,
                "personal_info": 0.0,
                "spam": 0.0,
                "troll": 1.0
              },
              "A_bare": 0.63
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
            "completion_tokens": 124,
            "finish_reason": "stop",
            "latency_s": 2.409188,
            "model": "gpt-6-luna",
            "prompt_tokens": 2946,
            "reasoning_tokens": 70
          },
          "error": null,
          "kind": "troll",
          "reason": "意味の取れない文字列のため、荒らしコメントとして判定しました。"
        }
      },
      "media_id": "local-U13",
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
      "text": "無無無無むむむ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.37941400200361386,
      "judge_s": 2.4092504819855094,
      "luna_s": 2.4092504819855094,
      "total_s": 2.4092549579800107,
      "writer_s": 4.475994501262903e-06
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
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "latency_s": 0.416031,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 149,
            "probabilities": {
              "A1": {
                "inappropriate": 0.04,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.96,
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
              "A_bare": 0.13
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
            "completion_tokens": 104,
            "finish_reason": "stop",
            "latency_s": 2.468633,
            "model": "gpt-6-luna",
            "prompt_tokens": 2947,
            "reasoning_tokens": 45
          },
          "error": null,
          "kind": "complaint",
          "reason": "問題そのものをけなすコメントのため、complaintです。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "言ってくれてありがとう、確認するね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "バカみたいな問題だな",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.41613512800540775,
      "judge_s": 2.468664315994829,
      "luna_s": 2.468664315994829,
      "total_s": 4.220871236000676,
      "writer_s": 1.7522069200058468
    }
  },
  {
    "case_id": "c-complaint-08",
    "record": {
      "comment_id": "c-complaint-08",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "latency_s": 0.388644,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 149,
            "probabilities": {
              "A1": {
                "inappropriate": 0.08,
                "other": 0.0,
                "question_or_guess": 0.19,
                "reaction": 0.73,
                "request": 0.0
              },
              "A2": {
                "chat": 0.03,
                "cheer": 0.0,
                "complaint": 0.67,
                "greeting": 0.0,
                "impression": 0.3,
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
            "completion_tokens": 271,
            "finish_reason": "stop",
            "latency_s": 3.361581,
            "model": "gpt-6-luna",
            "prompt_tokens": 2952,
            "reasoning_tokens": 205
          },
          "error": null,
          "kind": "complaint",
          "reason": "問題の表現への否定的な指摘で、作者個人への攻撃ではありません。"
        }
      },
      "media_id": "local-U13",
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
      "shadow_mismatch": false,
      "text": "そういう人たちを見下す感じ、無理",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.38880174298537895,
      "judge_s": 3.3616628700401634,
      "luna_s": 3.3616628700401634,
      "total_s": 4.326798268069979,
      "writer_s": 0.9651353980298154
    }
  },
  {
    "case_id": "c-spam-01",
    "record": {
      "comment_id": "c-spam-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "completion_tokens": 81,
            "finish_reason": "stop",
            "latency_s": 2.1024,
            "model": "gpt-6-luna",
            "prompt_tokens": 2948,
            "reasoning_tokens": 34
          },
          "error": null,
          "kind": "spam",
          "reason": "商品への誘導リンクを含む宣伝コメントです。"
        }
      },
      "media_id": "local-U13",
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
      "text": "新作はこちら https://example.invalid/deal",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 3.6807963624596596e-05,
      "judge_s": 2.1024670629994944,
      "luna_s": 2.1024670629994944,
      "total_s": 2.1024742950103246,
      "writer_s": 7.232010830193758e-06
    }
  },
  {
    "case_id": "c-spam-03",
    "record": {
      "comment_id": "c-spam-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1486,
            "latency_s": 0.509681,
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
              "A_bare": 0.05
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
            "completion_tokens": 91,
            "finish_reason": "stop",
            "latency_s": 1.718623,
            "model": "gpt-6-luna",
            "prompt_tokens": 2952,
            "reasoning_tokens": 39
          },
          "error": null,
          "kind": "spam",
          "reason": "副業への勧誘とプロフィールリンクへの誘導が含まれています。"
        }
      },
      "media_id": "local-U13",
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
      "text": "副業に興味ある人はプロフのリンクへ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.5098016979754902,
      "judge_s": 1.7186707640066743,
      "luna_s": 1.7186707640066743,
      "total_s": 1.7186733280541375,
      "writer_s": 2.5640474632382393e-06
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
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "completion_tokens": 90,
            "finish_reason": "stop",
            "latency_s": 2.617298,
            "model": "gpt-6-luna",
            "prompt_tokens": 2954,
            "reasoning_tokens": 38
          },
          "error": null,
          "kind": "spam",
          "reason": "プレゼント応募への誘導と外部リンクを含む宣伝コメントです。"
        }
      },
      "media_id": "local-U13",
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
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 2.902501728385687e-05,
      "judge_s": 2.6173456350225024,
      "luna_s": 2.6173456350225024,
      "total_s": 2.6173480240395293,
      "writer_s": 2.389017026871443e-06
    }
  },
  {
    "case_id": "c-personal_info-02",
    "record": {
      "comment_id": "c-personal_info-02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "personal_info"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1494,
            "latency_s": 0.435992,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
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
                "personal_info": 0.96,
                "spam": 0.04,
                "troll": 0.0
              },
              "A_bare": 0.07
            }
          },
          "error": null,
          "kind": "personal_info",
          "reason": "段A=inappropriate→personal_info"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 110,
            "finish_reason": "stop",
            "latency_s": 2.085529,
            "model": "gpt-6-luna",
            "prompt_tokens": 2949,
            "reasoning_tokens": 62
          },
          "error": null,
          "kind": "personal_info",
          "reason": "電話番号という個人情報を含むコメントのため。"
        }
      },
      "media_id": "local-U13",
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
      "text": "090-0000-0123 に電話ください",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.43606321804691106,
      "judge_s": 2.085571759031154,
      "luna_s": 2.085571759031154,
      "total_s": 2.0855746990418993,
      "writer_s": 2.9400107450783253e-06
    }
  },
  {
    "case_id": "c-personal_info-04",
    "record": {
      "comment_id": "c-personal_info-04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "personal_info"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1506,
            "latency_s": 0.382757,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
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
              "A_bare": 0.04
            }
          },
          "error": null,
          "kind": "personal_info",
          "reason": "段A=inappropriate→personal_info"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 99,
            "finish_reason": "stop",
            "latency_s": 1.688487,
            "model": "gpt-6-luna",
            "prompt_tokens": 2958,
            "reasoning_tokens": 49
          },
          "error": null,
          "kind": "personal_info",
          "reason": "本名と電話番号という個人情報が含まれています。"
        }
      },
      "media_id": "local-U13",
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
      "text": "本名はサンプル太郎、電話は090-0000-0456です",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.38315467198845,
      "judge_s": 1.688515426008962,
      "luna_s": 1.688515426008962,
      "total_s": 1.6885175320203416,
      "writer_s": 2.1060113795101643e-06
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
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "completion_tokens": 143,
            "finish_reason": "stop",
            "latency_s": 2.404894,
            "model": "gpt-6-luna",
            "prompt_tokens": 2943,
            "reasoning_tokens": 80
          },
          "error": null,
          "kind": "foreign",
          "reason": "英語のみのコメントのため、外国語として判定しました。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "日本語で質問してね！また遊ぼう☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "That was fun!",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 4.934496246278286e-05,
      "judge_s": 2.404962448985316,
      "luna_s": 2.404962448985316,
      "total_s": 4.368914577993564,
      "writer_s": 1.9639521290082484
    }
  },
  {
    "case_id": "c-foreign-03",
    "record": {
      "comment_id": "c-foreign-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 1,
            "input_tokens": 929,
            "latency_s": 0.207195,
            "major": "other",
            "model": "jev-latest",
            "output_tokens": 76,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.9,
                "question_or_guess": 0.0,
                "reaction": 0.1,
                "request": 0.0
              },
              "A_bare": 0.09
            }
          },
          "error": null,
          "kind": "foreign",
          "reason": "段A=other→foreign"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 113,
            "finish_reason": "stop",
            "latency_s": 2.138339,
            "model": "gpt-6-luna",
            "prompt_tokens": 2943,
            "reasoning_tokens": 46
          },
          "error": null,
          "kind": "foreign",
          "reason": "ひらがな・カタカナを含まない中国語のコメントです。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "日本語で質問してね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "这个好难啊",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.20727349299704656,
      "judge_s": 2.1384582919999957,
      "luna_s": 2.1384582919999957,
      "total_s": 3.3418074949877337,
      "writer_s": 1.203349202987738
    }
  },
  {
    "case_id": "c-foreign-05",
    "record": {
      "comment_id": "c-foreign-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 1,
            "input_tokens": 932,
            "latency_s": 0.199129,
            "major": "other",
            "model": "jev-latest",
            "output_tokens": 76,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.93,
                "question_or_guess": 0.0,
                "reaction": 0.07,
                "request": 0.0
              },
              "A_bare": 0.05
            }
          },
          "error": null,
          "kind": "foreign",
          "reason": "段A=other→foreign"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 152,
            "finish_reason": "stop",
            "latency_s": 2.325031,
            "model": "gpt-6-luna",
            "prompt_tokens": 2946,
            "reasoning_tokens": 88
          },
          "error": null,
          "kind": "foreign",
          "reason": "韓国語で書かれた、日本語以外のコメントです。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "日本語で質問してね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "이거 정말 재밌어요",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.1992857750155963,
      "judge_s": 2.3250880740233697,
      "luna_s": 2.3250880740233697,
      "total_s": 4.076222155999858,
      "writer_s": 1.7511340819764882
    }
  },
  {
    "case_id": "c-abuse-07",
    "record": {
      "comment_id": "c-abuse-07",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1490,
            "latency_s": 0.461653,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
            "probabilities": {
              "A1": {
                "inappropriate": 0.99,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.01,
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
            "completion_tokens": 98,
            "finish_reason": "stop",
            "latency_s": 1.727228,
            "model": "gpt-6-luna",
            "prompt_tokens": 2952,
            "reasoning_tokens": 48
          },
          "error": null,
          "kind": "abuse",
          "reason": "コメントしている人たちを侮辱する表現です。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "みんなが楽しめる言葉でお願いね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "ここでコメントしてる奴ら全員頭おかしい",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-09-30T16:34:53Z",
        "replied_at": null,
        "webhook_received_at": "2026-09-30T16:34:53Z"
      }
    },
    "timing": {
      "jev_s": 0.4617776150116697,
      "judge_s": 1.7272864819969982,
      "luna_s": 1.7272864819969982,
      "total_s": 1.7272940679686144,
      "writer_s": 7.585971616208553e-06
    }
  }
];
