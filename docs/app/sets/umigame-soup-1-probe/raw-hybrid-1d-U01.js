window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["hybrid-1d/U01"] = [
  {
    "case_id": "U01-e01",
    "record": {
      "comment_id": "U01-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 4163,
            "latency_s": 1.297861,
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
              "A_bare": 0.03,
              "B": {
                "point_0": 0.02,
                "point_1": 0.01
              },
              "C": 0.61,
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
            "completion_tokens": 170,
            "finish_reason": "stop",
            "latency_s": 3.597259,
            "model": "gpt-6-luna",
            "prompt_tokens": 2866,
            "reasoning_tokens": 95
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、太陽や照明でできる足元の影ではないとされています。"
        }
      },
      "media_id": "local-U01",
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
      "text": "男が言われた「影」って、足元にできる影なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2994230360200163,
      "judge_s": 3.597310593992006,
      "luna_s": 3.597310593992006,
      "total_s": 5.073457906983094,
      "writer_s": 1.4761473129910883
    }
  },
  {
    "case_id": "U01-e02",
    "record": {
      "comment_id": "U01-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 4103,
            "latency_s": 1.210876,
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
                "guess": 0.12,
                "question": 0.88
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
              "C": 0.29,
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
            "completion_tokens": 161,
            "finish_reason": "stop",
            "latency_s": 3.443359,
            "model": "gpt-6-luna",
            "prompt_tokens": 2859,
            "reasoning_tokens": 91
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "相手は男の家族ではないと確定事実にあります。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。その調子で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "あの相手は男の家族なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2111422420130111,
      "judge_s": 3.4433812180068344,
      "luna_s": 3.4433812180068344,
      "total_s": 4.528480778011726,
      "writer_s": 1.0850995600048918
    }
  },
  {
    "case_id": "U01-e03",
    "record": {
      "comment_id": "U01-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 4151,
            "latency_s": 1.220566,
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
                "guess": 0.1,
                "question": 0.9
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
              "C": 0.23,
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
            "completion_tokens": 155,
            "finish_reason": "stop",
            "latency_s": 3.676855,
            "model": "gpt-6-luna",
            "prompt_tokens": 2864,
            "reasoning_tokens": 76
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、男は以前から相手のところへ定期的に通っていたとあります。"
        }
      },
      "media_id": "local-U01",
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
      "text": "男はその相手のところに定期的に通ってた？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2208937980176415,
      "judge_s": 3.6769000560161658,
      "luna_s": 3.6769000560161658,
      "total_s": 4.669603423011722,
      "writer_s": 0.9927033669955563
    }
  },
  {
    "case_id": "U01-e04",
    "record": {
      "comment_id": "U01-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 4115,
            "latency_s": 1.18435,
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
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01,
                "point_1": 0.02
              },
              "C": 0.27,
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
            "completion_tokens": 383,
            "finish_reason": "stop",
            "latency_s": 5.551,
            "model": "gpt-6-luna",
            "prompt_tokens": 2859,
            "reasoning_tokens": 319
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、男は入院していないとあります。"
        }
      },
      "media_id": "local-U01",
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
      "text": "男はその場所に入院してたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1846570600173436,
      "judge_s": 5.5510419480269775,
      "luna_s": 5.5510419480269775,
      "total_s": 8.628119548026007,
      "writer_s": 3.077077599999029
    }
  },
  {
    "case_id": "U01-e05",
    "record": {
      "comment_id": "U01-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 4157,
            "latency_s": 1.267366,
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
                "guess": 0.75,
                "question": 0.25
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.03,
                "q_yesno": 0.96
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.01,
                "point_1": 0.01
              },
              "C": 0.4,
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
            "completion_tokens": 266,
            "finish_reason": "stop",
            "latency_s": 3.579603,
            "model": "gpt-6-luna",
            "prompt_tokens": 2863,
            "reasoning_tokens": 189
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実では、涙は良い知らせを聞いたうれし涙です。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。今日泣いたのは、悪い知らせを聞いたからじゃないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "今日泣いたのは、悪い知らせを聞いたから？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2676530930039007,
      "judge_s": 3.5796476249815896,
      "luna_s": 3.5796476249815896,
      "total_s": 5.499246322986437,
      "writer_s": 1.9195986980048474
    }
  },
  {
    "case_id": "U01-e06",
    "record": {
      "comment_id": "U01-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 4121,
            "latency_s": 1.385913,
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
                "guess": 0.72,
                "question": 0.28
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
              "C": 0.52,
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
            "completion_tokens": 191,
            "finish_reason": "stop",
            "latency_s": 2.688585,
            "model": "gpt-6-luna",
            "prompt_tokens": 2860,
            "reasoning_tokens": 126
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、相手は男をからかったり意地悪で言ったりしていません。"
        }
      },
      "media_id": "local-U01",
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
      "text": "相手は男をからかって言ったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.3862301019835286,
      "judge_s": 2.688617817009799,
      "luna_s": 2.688617817009799,
      "total_s": 6.7986801470106,
      "writer_s": 4.110062330000801
    }
  },
  {
    "case_id": "U01-e07",
    "record": {
      "comment_id": "U01-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 4109,
            "latency_s": 1.176688,
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
                "point_0": 0.01,
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
            "completion_tokens": 169,
            "finish_reason": "stop",
            "latency_s": 2.054945,
            "model": "gpt-6-luna",
            "prompt_tokens": 2859,
            "reasoning_tokens": 97
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、相手は男の友だちではないと示されています。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。相手は男の友だちじゃないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "相手は男の友だちだったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1769657750264741,
      "judge_s": 2.054996847989969,
      "luna_s": 2.054996847989969,
      "total_s": 4.383727560983971,
      "writer_s": 2.328730712994002
    }
  },
  {
    "case_id": "U01-e08",
    "record": {
      "comment_id": "U01-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 4091,
            "latency_s": 1.24869,
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
                "guess": 0.06,
                "question": 0.94
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
              "C": 0.24,
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
            "completion_tokens": 141,
            "finish_reason": "stop",
            "latency_s": 2.102365,
            "model": "gpt-6-luna",
            "prompt_tokens": 2855,
            "reasoning_tokens": 70
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "男の職業は問題の答えに関係しないと明記されています。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ほかにも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は会社員だったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2489817940222565,
      "judge_s": 2.1024106180120725,
      "luna_s": 2.1024106180120725,
      "total_s": 3.3503880000207573,
      "writer_s": 1.2479773820086848
    }
  },
  {
    "case_id": "U01-e09",
    "record": {
      "comment_id": "U01-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 4193,
            "latency_s": 1.150858,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 256,
            "probabilities": {
              "A1": {
                "inappropriate": 0.03,
                "other": 0.0,
                "question_or_guess": 0.91,
                "reaction": 0.06,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.68,
                "question": 0.32
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.02,
                "q_yesno": 0.98
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.04,
                "point_1": 0.02
              },
              "C": 0.32,
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
            "completion_tokens": 193,
            "finish_reason": "stop",
            "latency_s": 2.179456,
            "model": "gpt-6-luna",
            "prompt_tokens": 2870,
            "reasoning_tokens": 113
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、以前影が濃くなったと分かり、ひどく落ち込んだとあります。"
        }
      },
      "media_id": "local-U01",
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
      "text": "男は以前、影が濃くなったと知って落ち込んだことある？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1511280120175797,
      "judge_s": 2.179494618991157,
      "luna_s": 2.179494618991157,
      "total_s": 3.3488445809925906,
      "writer_s": 1.1693499620014336
    }
  },
  {
    "case_id": "U01-e10",
    "record": {
      "comment_id": "U01-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 4181,
            "latency_s": 2.322248,
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
                "q_open": 0.03,
                "q_yesno": 0.97
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01,
                "point_1": 0.13
              },
              "C": 0.54,
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
            "completion_tokens": 241,
            "finish_reason": "stop",
            "latency_s": 4.113673,
            "model": "gpt-6-luna",
            "prompt_tokens": 2869,
            "reasoning_tokens": 165
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "相手が笑っていたのは、良い知らせを伝えられたからと確定しています。"
        }
      },
      "media_id": "local-U01",
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
      "text": "相手が笑ったのは、男に良い知らせを伝えられたから？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 2.3225422039977275,
      "judge_s": 4.113705787982326,
      "luna_s": 4.113705787982326,
      "total_s": 5.391181330982363,
      "writer_s": 1.2774755430000369
    }
  },
  {
    "case_id": "U01-e11",
    "record": {
      "comment_id": "U01-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 2127,
            "latency_s": 0.589865,
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
                "guess": 0.88,
                "question": 0.12
              },
              "A2": {
                "q_multi": 0.88,
                "q_open": 0.01,
                "q_yesno": 0.11
              },
              "A_bare": 0.03
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
            "completion_tokens": 186,
            "finish_reason": "stop",
            "latency_s": 2.148202,
            "model": "gpt-6-luna",
            "prompt_tokens": 2866,
            "reasoning_tokens": 109
          },
          "error": null,
          "kind": "q_multi",
          "reason": "相手の職業と影が薄くなった理由の二点を尋ねています。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。まずはどちらから聞こうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "相手ってお医者さん？それで影が薄くなったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.5900313800084405,
      "judge_s": 2.148281964007765,
      "luna_s": 2.148281964007765,
      "total_s": 5.66926963601145,
      "writer_s": 3.5209876720036846
    }
  },
  {
    "case_id": "U01-e12",
    "record": {
      "comment_id": "U01-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "latency_s": 0.56005,
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
                "guess": 0.02,
                "question": 0.98
              },
              "A2": {
                "q_multi": 0.93,
                "q_open": 0.07,
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
            "completion_tokens": 153,
            "finish_reason": "stop",
            "latency_s": 2.124363,
            "model": "gpt-6-luna",
            "prompt_tokens": 2864,
            "reasoning_tokens": 79
          },
          "error": null,
          "kind": "q_multi",
          "reason": "通っていた場所と相手の正体について、質問が二つあります。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつ聞いてごらん。まずはどっちからにしようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男はどこに通ってたの？相手は誰なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.5602718250011094,
      "judge_s": 2.1244209760043304,
      "luna_s": 2.1244209760043304,
      "total_s": 3.69723994701053,
      "writer_s": 1.5728189710061997
    }
  },
  {
    "case_id": "U01-e13",
    "record": {
      "comment_id": "U01-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "latency_s": 0.920314,
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
                "guess": 0.03,
                "question": 0.97
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.99,
                "q_yesno": 0.0
              },
              "A3": 0.03,
              "A_bare": 0.02
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
            "completion_tokens": 167,
            "finish_reason": "stop",
            "latency_s": 2.246972,
            "model": "gpt-6-luna",
            "prompt_tokens": 2869,
            "reasoning_tokens": 87
          },
          "error": null,
          "kind": "q_open",
          "reason": "理由を尋ねる質問で、はい／いいえでは答えられません。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "男が泣いて何度も頭を下げた理由を、はい・いいえで答えられる質問にして聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "なんで男はあんなに泣いて、何度も頭を下げたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.9204785550246015,
      "judge_s": 2.247025229007704,
      "luna_s": 2.247025229007704,
      "total_s": 5.4444625999894924,
      "writer_s": 3.1974373709817883
    }
  },
  {
    "case_id": "U01-e14",
    "record": {
      "comment_id": "U01-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "latency_s": 0.836913,
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
            "completion_tokens": 223,
            "finish_reason": "stop",
            "latency_s": 2.285395,
            "model": "gpt-6-luna",
            "prompt_tokens": 2862,
            "reasoning_tokens": 138
          },
          "error": null,
          "kind": "q_open",
          "reason": "「どうして」と理由を尋ねており、はい／いいえで答えられない質問です。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "相手もにこにこ笑っていたのは、何か理由があるのかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "どうして相手もにこにこ笑ってたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.8371556730126031,
      "judge_s": 2.285452462005196,
      "luna_s": 2.285452462005196,
      "total_s": 6.198414072016021,
      "writer_s": 3.912961610010825
    }
  },
  {
    "case_id": "U01-e15",
    "record": {
      "comment_id": "U01-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 2626,
            "latency_s": 0.787571,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 178,
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
                "q_multi": 0.01,
                "q_open": 0.21,
                "q_yesno": 0.78
              },
              "A3": 0.52,
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.52"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 293,
            "finish_reason": "stop",
            "latency_s": 3.768422,
            "model": "gpt-6-luna",
            "prompt_tokens": 2861,
            "reasoning_tokens": 201
          },
          "error": null,
          "kind": "q_open",
          "reason": "「あの人」と「それ」が誰・何を指すか一意に決まりません。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "誰のことかも書いて、はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "あの人はそれを見て嬉しかったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.7877691189933103,
      "judge_s": 3.7684850159857888,
      "luna_s": 3.7684850159857888,
      "total_s": 7.904893149971031,
      "writer_s": 4.136408133985242
    }
  },
  {
    "case_id": "U01-e16",
    "record": {
      "comment_id": "U01-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 2189,
            "latency_s": 0.73778,
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
                "point_0": 0.89,
                "point_1": 0.96
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
            "completion_tokens": 206,
            "finish_reason": "stop",
            "latency_s": 2.094723,
            "model": "gpt-6-luna",
            "prompt_tokens": 2909,
            "reasoning_tokens": 98
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "レントゲンの影と病気の回復、主治医への感謝まで言い当てています。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！男の「影」はレントゲンに写った病気の跡。3か月ぶりの診察で回復を知り、主治医に感謝した。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男の「影」はレントゲン写真に写った病気の跡で、3か月ぶりの診察で薄くなったと主治医に聞いて回復を喜び、治療への感謝で頭を下げたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.7380969529913273,
      "judge_s": 2.094776258978527,
      "luna_s": 2.094776258978527,
      "total_s": 2.094788083981257,
      "writer_s": 1.182500272989273e-05
    }
  },
  {
    "case_id": "U01-e17",
    "record": {
      "comment_id": "U01-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 2117,
            "latency_s": 0.870369,
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
                "point_0": 0.73,
                "point_1": 0.89
              }
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.73"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 264,
            "finish_reason": "stop",
            "latency_s": 2.822069,
            "model": "gpt-6-luna",
            "prompt_tokens": 2884,
            "reasoning_tokens": 153
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "レントゲンの影と病気の回復、医師への感謝まで核心を言い当てています。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！男の「影」はレントゲンに写った病気の跡。3か月ぶりの診察で回復を知り、主治医に感謝した。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男の影はレントゲンに写る病気の跡で、主治医から回復の知らせを聞いて感謝した、ってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.870583068986889,
      "judge_s": 2.822134134999942,
      "luna_s": 2.822134134999942,
      "total_s": 2.822138638002798,
      "writer_s": 4.503002855926752e-06
    }
  },
  {
    "case_id": "U01-e18",
    "record": {
      "comment_id": "U01-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 2084,
            "latency_s": 0.594652,
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
              "A_bare": 0.03,
              "B": {
                "point_0": 0.93,
                "point_1": 0.02
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
            "completion_tokens": 429,
            "finish_reason": "stop",
            "latency_s": 3.863428,
            "model": "gpt-6-luna",
            "prompt_tokens": 2876,
            "reasoning_tokens": 363
          },
          "error": null,
          "kind": "guess_close",
          "reason": "レントゲンの影には触れていますが、病気が良くなった点までは言えていません。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！ほかの可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "影ってレントゲンに写る影のことでしょ。男は医者に何か言われたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.5948657949920744,
      "judge_s": 3.86347304697847,
      "luna_s": 3.86347304697847,
      "total_s": 5.569005053985165,
      "writer_s": 1.7055320070066955
    }
  },
  {
    "case_id": "U01-e19",
    "record": {
      "comment_id": "U01-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 2075,
            "latency_s": 0.603381,
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
                "point_0": 0.16,
                "point_1": 0.92
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.16"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 295,
            "finish_reason": "stop",
            "latency_s": 3.138584,
            "model": "gpt-6-luna",
            "prompt_tokens": 2873,
            "reasoning_tokens": 218
          },
          "error": null,
          "kind": "guess_close",
          "reason": "病気が良くなった点には触れていますが、影の正体が含まれていません。"
        }
      },
      "media_id": "local-U01",
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
      "text": "影が薄くなったのは、男の病気が良くなってきた知らせなんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.6035827200103085,
      "judge_s": 3.1386336809955537,
      "luna_s": 3.1386336809955537,
      "total_s": 4.552641217014752,
      "writer_s": 1.4140075360191986
    }
  },
  {
    "case_id": "U01-e20",
    "record": {
      "comment_id": "U01-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 2629,
            "latency_s": 0.856415,
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
            "completion_tokens": 192,
            "finish_reason": "stop",
            "latency_s": 2.407078,
            "model": "gpt-6-luna",
            "prompt_tokens": 2876,
            "reasoning_tokens": 118
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "影を存在感と捉え、涙も悔し涙とする推理で、仕掛けの核心には触れていません。"
        }
      },
      "media_id": "local-U01",
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
      "text": "男は存在感が薄いと嫌味を言われ、悔しくて泣きながら帰ったんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.856615870987298,
      "judge_s": 2.407137172995135,
      "luna_s": 2.407137172995135,
      "total_s": 3.402072027005488,
      "writer_s": 0.9949348540103529
    }
  },
  {
    "case_id": "U01-e21",
    "record": {
      "comment_id": "U01-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 2613,
            "latency_s": 0.901703,
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
                "q_open": 0.82,
                "q_yesno": 0.16
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01,
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
            "completion_tokens": 242,
            "finish_reason": "stop",
            "latency_s": 2.643776,
            "model": "gpt-6-luna",
            "prompt_tokens": 2874,
            "reasoning_tokens": 174
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "影の正体や病気の回復には触れず、確定事実とも反する推理です。"
        }
      },
      "media_id": "local-U01",
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
      "text": "相手は男をからかって笑い、男は怒って何度も頭を下げたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.9019593950069975,
      "judge_s": 2.64385263499571,
      "luna_s": 2.64385263499571,
      "total_s": 3.5292449349944945,
      "writer_s": 0.8853922999987844
    }
  },
  {
    "case_id": "U01-b22",
    "record": {
      "comment_id": "U01-b22",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 4115,
            "latency_s": 1.190015,
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
                "q_open": 0.03,
                "q_yesno": 0.97
              },
              "A_bare": 0.05,
              "B": {
                "point_0": 0.02,
                "point_1": 0.01
              },
              "C": 0.37,
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
            "completion_tokens": 162,
            "finish_reason": "stop",
            "latency_s": 1.993051,
            "model": "gpt-6-luna",
            "prompt_tokens": 2858,
            "reasoning_tokens": 92
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、「影」は男の存在感ではないと示されています。"
        }
      },
      "media_id": "local-U01",
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
      "text": "「影」って存在感のことなの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1903767389885616,
      "judge_s": 1.9930838810105342,
      "luna_s": 1.9930838810105342,
      "total_s": 2.9716558679938316,
      "writer_s": 0.9785719869832974
    }
  },
  {
    "case_id": "U01-b23",
    "record": {
      "comment_id": "U01-b23",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 4127,
            "latency_s": 1.207949,
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
                "guess": 0.24,
                "question": 0.76
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.04,
              "B": {
                "point_0": 0.04,
                "point_1": 0.08
              },
              "C": 0.47,
              "D": {
                "irrelevant": 0.0,
                "no": 0.57,
                "yes": 0.43
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.04"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 1723,
            "finish_reason": "stop",
            "latency_s": 13.231576,
            "model": "gpt-6-luna",
            "prompt_tokens": 2863,
            "reasoning_tokens": 1629
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "単なる外見の変化ではなく、病状の改善を示す変化のため。"
        }
      },
      "media_id": "local-U01",
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
      "text": "影が薄くなったのは見た目の変化？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.208229723997647,
      "judge_s": 13.231632620998425,
      "luna_s": 13.231632620998425,
      "total_s": 16.264738386002136,
      "writer_s": 3.033105765003711
    }
  },
  {
    "case_id": "U01-b24",
    "record": {
      "comment_id": "U01-b24",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 4079,
            "latency_s": 1.184621,
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
                "guess": 0.46,
                "question": 0.54
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
              "C": 0.43,
              "D": {
                "irrelevant": 0.05,
                "no": 0.04,
                "yes": 0.91
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
            "completion_tokens": 195,
            "finish_reason": "stop",
            "latency_s": 2.602305,
            "model": "gpt-6-luna",
            "prompt_tokens": 2855,
            "reasoning_tokens": 136
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "相手は真相で男の主治医と明かされているためです。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！相手は医者だよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "相手は医者なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1849506839935202,
      "judge_s": 2.6023563019989524,
      "luna_s": 2.6023563019989524,
      "total_s": 6.203025769995293,
      "writer_s": 3.6006694679963402
    }
  },
  {
    "case_id": "U01-b25",
    "record": {
      "comment_id": "U01-b25",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 4109,
            "latency_s": 1.261326,
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
                "guess": 0.67,
                "question": 0.33
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
              "C": 0.47,
              "D": {
                "irrelevant": 0.02,
                "no": 0.01,
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
            "completion_tokens": 194,
            "finish_reason": "stop",
            "latency_s": 2.362437,
            "model": "gpt-6-luna",
            "prompt_tokens": 2861,
            "reasoning_tokens": 115
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "真相に治療を続けていたとあるため、治療を受けていたかは「はい」です。"
        }
      },
      "media_id": "local-U01",
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
      "text": "男は何かの治療を受けてた？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2616560150054283,
      "judge_s": 2.362496004003333,
      "luna_s": 2.362496004003333,
      "total_s": 3.316190543002449,
      "writer_s": 0.953694538999116
    }
  },
  {
    "case_id": "U01-b26",
    "record": {
      "comment_id": "U01-b26",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 4109,
            "latency_s": 1.277636,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 256,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.01,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.64,
                "question": 0.36
              },
              "A2": {
                "q_multi": 0.16,
                "q_open": 0.02,
                "q_yesno": 0.82
              },
              "A_bare": 0.04,
              "B": {
                "point_0": 0.01,
                "point_1": 0.01
              },
              "C": 0.36,
              "D": {
                "irrelevant": 0.01,
                "no": 0.97,
                "yes": 0.02
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
            "completion_tokens": 269,
            "finish_reason": "stop",
            "latency_s": 2.873343,
            "model": "gpt-6-luna",
            "prompt_tokens": 2858,
            "reasoning_tokens": 193
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "問題の状況を舞台や撮影の話か尋ねる質問で、真相とは異なります。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。次の質問もしてごらん"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "これって舞台とか撮影の話？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2779818209819496,
      "judge_s": 2.8733958519878797,
      "luna_s": 2.8733958519878797,
      "total_s": 6.47251551298541,
      "writer_s": 3.5991196609975304
    }
  },
  {
    "case_id": "U01-b27",
    "record": {
      "comment_id": "U01-b27",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 4121,
            "latency_s": 2.269248,
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
                "guess": 0.77,
                "question": 0.23
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.04,
              "B": {
                "point_0": 0.01,
                "point_1": 0.02
              },
              "C": 0.47,
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
            "completion_tokens": 555,
            "finish_reason": "stop",
            "latency_s": 5.009662,
            "model": "gpt-6-luna",
            "prompt_tokens": 2860,
            "reasoning_tokens": 477
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "感謝のために頭を下げたという確定事実に合う質問です。"
        }
      },
      "media_id": "local-U01",
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
      "text": "相手にお礼を言ってるってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 2.2695709989930037,
      "judge_s": 5.0097113529918715,
      "luna_s": 5.0097113529918715,
      "total_s": 6.114544080977794,
      "writer_s": 1.1048327279859222
    }
  },
  {
    "case_id": "U01-e28",
    "record": {
      "comment_id": "U01-e28",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 2171,
            "latency_s": 0.567888,
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
                "guess": 0.96,
                "question": 0.04
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.93,
                "point_1": 0.96
              }
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.93"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 225,
            "finish_reason": "stop",
            "latency_s": 3.081488,
            "model": "gpt-6-luna",
            "prompt_tokens": 2898,
            "reasoning_tokens": 156
          },
          "error": null,
          "kind": "guess_close",
          "reason": "影が薄くなって病気が良くなった点は合っていますが、相手の人物像に誤りがあります。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し考えてみようか☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "レントゲンの影が薄くなって病気は良くなったんだね。でも相手は治療してくれた医者じゃなくて、たまたま会った近所の人だったのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.5681068109988701,
      "judge_s": 3.0815203139791265,
      "luna_s": 3.0815203139791265,
      "total_s": 6.417164107988356,
      "writer_s": 3.335643794009229
    }
  },
  {
    "case_id": "U01-t01",
    "record": {
      "comment_id": "U01-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "58478bf2d8f9",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "レントゲン",
          "debug": {
            "calls": 1,
            "input_tokens": 930,
            "latency_s": 0.197668,
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
          "bare_term": "レントゲン",
          "debug": {
            "completion_tokens": 195,
            "finish_reason": "stop",
            "latency_s": 2.093685,
            "model": "gpt-6-luna",
            "prompt_tokens": 2853,
            "reasoning_tokens": 113
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない名詞だけのコメントなので、q_openです。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "レントゲンがどうしたのか聞かせてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "レントゲン？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.19779460702557117,
      "judge_s": 2.0937441429996397,
      "luna_s": 2.0937441429996397,
      "total_s": 4.954411529004574,
      "writer_s": 2.860667386004934
    }
  },
  {
    "case_id": "U01-t02",
    "record": {
      "comment_id": "U01-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "58478bf2d8f9",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "病院",
          "debug": {
            "calls": 1,
            "input_tokens": 926,
            "latency_s": 0.188306,
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
              "A_bare": 0.98
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.98"
        },
        "luna": {
          "answer": null,
          "bare_term": "病院",
          "debug": {
            "completion_tokens": 195,
            "finish_reason": "stop",
            "latency_s": 2.388458,
            "model": "gpt-6-luna",
            "prompt_tokens": 2850,
            "reasoning_tokens": 113
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない名詞だけのコメントなので、語句のみとして扱います。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "病院がどうしたのか聞かせてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "病院",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.18841890699695796,
      "judge_s": 2.3885130290000234,
      "luna_s": 2.3885130290000234,
      "total_s": 7.849623905000044,
      "writer_s": 5.461110876000021
    }
  },
  {
    "case_id": "U01-t03",
    "record": {
      "comment_id": "U01-t03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "58478bf2d8f9",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "影",
          "debug": {
            "calls": 1,
            "input_tokens": 926,
            "latency_s": 0.225629,
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
          "bare_term": "影",
          "debug": {
            "completion_tokens": 229,
            "finish_reason": "stop",
            "latency_s": 2.795457,
            "model": "gpt-6-luna",
            "prompt_tokens": 2850,
            "reasoning_tokens": 144
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句だけのコメントなので、答えを特定できない質問です。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "何が影なのか教えてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "影？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.22574715298833326,
      "judge_s": 2.7954998560016975,
      "luna_s": 2.7954998560016975,
      "total_s": 7.896654773998307,
      "writer_s": 5.10115491799661
    }
  },
  {
    "case_id": "c-ask_hint-01",
    "record": {
      "comment_id": "c-ask_hint-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 1421,
            "latency_s": 0.41181,
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
              "A_bare": 0.31
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
            "completion_tokens": 236,
            "finish_reason": "stop",
            "latency_s": 7.813402,
            "model": "gpt-6-luna",
            "prompt_tokens": 2852,
            "reasoning_tokens": 150
          },
          "error": null,
          "kind": "ask_hint",
          "reason": "ヒントを求めているため、質問で絞るよう促します。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ヒントは出せないけど、質問で少しずつ絞っていこうね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "ヒントください！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.4119121670082677,
      "judge_s": 7.813452843023697,
      "luna_s": 7.813452843023697,
      "total_s": 11.196492627030239,
      "writer_s": 3.3830397840065416
    }
  },
  {
    "case_id": "c-ask_howto-05",
    "record": {
      "comment_id": "c-ask_howto-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "calls": 2,
            "input_tokens": 1433,
            "latency_s": 0.405506,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 124,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.02,
                "reaction": 0.0,
                "request": 0.98
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
            "completion_tokens": 270,
            "finish_reason": "stop",
            "latency_s": 2.819764,
            "model": "gpt-6-luna",
            "prompt_tokens": 2860,
            "reasoning_tokens": 189
          },
          "error": null,
          "kind": "q_multi",
          "reason": "中の人かどうかと自動返信かどうか、質問が二つあります。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。どっちから聞こうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "これ中の人？自動で返してる？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.40558977000182495,
      "judge_s": 2.8198174700082745,
      "luna_s": 2.8198174700082745,
      "total_s": 4.194757461023983,
      "writer_s": 1.374939991015708
    }
  },
  {
    "case_id": "c-cheer-04",
    "record": {
      "comment_id": "c-cheer-04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 1592,
            "latency_s": 0.404016,
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
                "chat": 0.0,
                "cheer": 1.0,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.0,
                "mention": 0.0,
                "request": 0.0
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
            "completion_tokens": 194,
            "finish_reason": "stop",
            "latency_s": 2.210876,
            "model": "gpt-6-luna",
            "prompt_tokens": 2859,
            "reasoning_tokens": 130
          },
          "error": null,
          "kind": "cheer",
          "reason": "継続して見ていることを伝え、頑張るよう応援しているコメントです。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いつも見てくれてありがとう！これからもがんばるね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "いつも見てるよ、がんばって",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.40417911199619994,
      "judge_s": 2.2109240950085223,
      "luna_s": 2.2109240950085223,
      "total_s": 4.455072778015165,
      "writer_s": 2.2441486830066424
    }
  },
  {
    "case_id": "c-complaint-03",
    "record": {
      "comment_id": "c-complaint-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "latency_s": 0.378657,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 150,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.05,
                "reaction": 0.86,
                "request": 0.09
              },
              "A2": {
                "chat": 0.0,
                "cheer": 0.0,
                "complaint": 0.47,
                "greeting": 0.0,
                "impression": 0.53,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.05
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
            "completion_tokens": 245,
            "finish_reason": "stop",
            "latency_s": 2.615559,
            "model": "gpt-6-luna",
            "prompt_tokens": 2862,
            "reasoning_tokens": 178
          },
          "error": null,
          "kind": "complaint",
          "reason": "答えを聞いても腑に落ちないという、問題への不満・指摘です。"
        }
      },
      "media_id": "local-U01",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "コメントありがとう、確認するね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "答えを聞いても腑に落ちないかも",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.37880926197976805,
      "judge_s": 2.6156132470059674,
      "luna_s": 2.6156132470059674,
      "total_s": 6.325364215997979,
      "writer_s": 3.7097509689920116
    }
  },
  {
    "case_id": "c-troll-02",
    "record": {
      "comment_id": "c-troll-02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "input_tokens": 1464,
            "latency_s": 0.400478,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
            "probabilities": {
              "A1": {
                "inappropriate": 0.71,
                "other": 0.27,
                "question_or_guess": 0.02,
                "reaction": 0.0,
                "request": 0.0
              },
              "A2": {
                "abuse": 0.0,
                "personal_info": 0.0,
                "spam": 0.0,
                "troll": 1.0
              },
              "A_bare": 0.79
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
            "completion_tokens": 120,
            "finish_reason": "stop",
            "latency_s": 1.834803,
            "model": "gpt-6-luna",
            "prompt_tokens": 2854,
            "reasoning_tokens": 64
          },
          "error": null,
          "kind": "troll",
          "reason": "意味の取れない英字の文字列で、問題への推理として判断できません。"
        }
      },
      "media_id": "local-U01",
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
      "text": "QWERTYZZZ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.40063840098446235,
      "judge_s": 1.8348636069858912,
      "luna_s": 1.8348636069858912,
      "total_s": 1.8348668749968056,
      "writer_s": 3.268010914325714e-06
    }
  },
  {
    "case_id": "c-personal_info-01",
    "record": {
      "comment_id": "c-personal_info-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "001-faint-shadow",
      "errors": [],
      "fact_sheet_hash": "58478bf2d8f9",
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
            "latency_s": 0.398647,
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
                "personal_info": 0.99,
                "spam": 0.01,
                "troll": 0.0
              },
              "A_bare": 0.1
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
            "completion_tokens": 90,
            "finish_reason": "stop",
            "latency_s": 6.776725,
            "model": "gpt-6-luna",
            "prompt_tokens": 2861,
            "reasoning_tokens": 41
          },
          "error": null,
          "kind": "personal_info",
          "reason": "電話番号と思われる個人情報が含まれています。"
        }
      },
      "media_id": "local-U01",
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
      "text": "連絡先これです 090-0000-0001",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.39880912299850024,
      "judge_s": 6.77678093497525,
      "luna_s": 6.77678093497525,
      "total_s": 6.776784552959725,
      "writer_s": 3.617984475567937e-06
    }
  }
];
