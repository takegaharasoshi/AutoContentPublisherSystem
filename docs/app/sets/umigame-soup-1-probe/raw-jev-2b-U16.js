window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["jev-2b/U16"] = [
  {
    "case_id": "U16-e01",
    "record": {
      "comment_id": "U16-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 4300,
            "latency_s": 1.226096,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
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
              "A_bare": 0.02,
              "B": {
                "point_0": 0.13
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
          "reason": "段A=question→q_yesno, 要点最低=0.13"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "いいえ。なるほど、メモしておくね🧐"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は本当に体が凍って動けなくなっているんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.226424019987462,
      "judge_s": 1.226424019987462,
      "luna_s": null,
      "total_s": 1.2264254270121455,
      "writer_s": 1.407024683430791e-06
    }
  },
  {
    "case_id": "U16-e02",
    "record": {
      "comment_id": "U16-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 4270,
            "latency_s": 1.129113,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
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
                "q_multi": 0.1,
                "q_open": 0.0,
                "q_yesno": 0.9
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02
              },
              "C": 0.45,
              "D": {
                "irrelevant": 0.2,
                "no": 0.8,
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
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "いいえ。まだまだ聞いていいんだよ😌"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "そこは外で、気温がかなり低い場所ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1293388969788793,
      "judge_s": 1.1293388969788793,
      "luna_s": null,
      "total_s": 1.129340504994616,
      "writer_s": 1.6080157365649939e-06
    }
  },
  {
    "case_id": "U16-e03",
    "record": {
      "comment_id": "U16-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 4300,
            "latency_s": 1.233151,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
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
                "q_multi": 0.05,
                "q_open": 0.01,
                "q_yesno": 0.94
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.03
              },
              "C": 0.49,
              "D": {
                "irrelevant": 0.01,
                "no": 0.31,
                "yes": 0.68
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.03"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい！ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は生きていて、助けが来るのを待っているんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2333358739851974,
      "judge_s": 1.2333358739851974,
      "luna_s": null,
      "total_s": 1.2333376839815173,
      "writer_s": 1.8099963199347258e-06
    }
  },
  {
    "case_id": "U16-e04",
    "record": {
      "comment_id": "U16-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 4252,
            "latency_s": 1.138475,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
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
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02
              },
              "C": 0.32,
              "D": {
                "irrelevant": 0.01,
                "no": 0.0,
                "yes": 0.99
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい！さあ、次はなにを聞く？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "助けに来た女は男の知り合いですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1386434129963163,
      "judge_s": 1.1386434129963163,
      "luna_s": null,
      "total_s": 1.1386448389966972,
      "writer_s": 1.4260003808885813e-06
    }
  },
  {
    "case_id": "U16-e05",
    "record": {
      "comment_id": "U16-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 4276,
            "latency_s": 1.185328,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.55,
                "question": 0.45
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.06
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
          "reason": "段A=question→q_yesno, 要点最低=0.06"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい！まだまだ聞いていいんだよ😌"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "女も男と同じ原因で動けなくなったんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1854854690027423,
      "judge_s": 1.1854854690027423,
      "luna_s": null,
      "total_s": 1.1854869489907287,
      "writer_s": 1.4799879863858223e-06
    }
  },
  {
    "case_id": "U16-e06",
    "record": {
      "comment_id": "U16-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 4240,
            "latency_s": 1.129641,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.44,
                "question": 0.56
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.02
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
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "いいえ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "二人は雪山にいるんでしょうか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1298558530106675,
      "judge_s": 1.1298558530106675,
      "luna_s": null,
      "total_s": 1.1298573370149825,
      "writer_s": 1.4840043149888515e-06
    }
  },
  {
    "case_id": "U16-e07",
    "record": {
      "comment_id": "U16-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 4264,
            "latency_s": 1.231323,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.82,
                "question": 0.18
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.09
              },
              "C": 0.72,
              "D": {
                "irrelevant": 0.05,
                "no": 0.95,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.09"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "いいえ。次の質問も待ってるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男と女は氷の上に立っているんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.231521123991115,
      "judge_s": 1.231521123991115,
      "luna_s": null,
      "total_s": 1.2315225040074438,
      "writer_s": 1.380016328766942e-06
    }
  },
  {
    "case_id": "U16-e08",
    "record": {
      "comment_id": "U16-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 4288,
            "latency_s": 1.221901,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.23,
                "question": 0.77
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02
              },
              "C": 0.3,
              "D": {
                "irrelevant": 0.0,
                "no": 0.02,
                "yes": 0.98
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "誰かが二人を助けに来る可能性はまだありますか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.22214337499463,
      "judge_s": 1.22214337499463,
      "luna_s": null,
      "total_s": 1.2221448489872273,
      "writer_s": 1.4739925973117352e-06
    }
  },
  {
    "case_id": "U16-e09",
    "record": {
      "comment_id": "U16-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 4258,
            "latency_s": 1.26776,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.68,
                "question": 0.32
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02
              },
              "C": 0.68,
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
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "いいえ。まだまだ聞いていいんだよ😌"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男はけがをしていて動けないんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.268032759980997,
      "judge_s": 1.268032759980997,
      "luna_s": null,
      "total_s": 1.2680341889790725,
      "writer_s": 1.4289980754256248e-06
    }
  },
  {
    "case_id": "U16-e10",
    "record": {
      "comment_id": "U16-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 4294,
            "latency_s": 1.293931,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
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
                "q_multi": 0.0,
                "q_open": 0.02,
                "q_yesno": 0.98
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.16
              },
              "C": 0.56,
              "D": {
                "irrelevant": 0.0,
                "no": 1.0,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.16"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "いいえ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "二人が凍りついたのは、寒さのせいなんでしょか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.294157800002722,
      "judge_s": 1.294157800002722,
      "luna_s": null,
      "total_s": 1.294159144978039,
      "writer_s": 1.3449753168970346e-06
    }
  },
  {
    "case_id": "U16-e11",
    "record": {
      "comment_id": "U16-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 2132,
            "latency_s": 0.647445,
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
                "guess": 0.74,
                "question": 0.26
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
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "欲張らずに 1 つずつ聞いてごらん😉"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は雪で遭難したの？女も同じ場所で遭難したの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.6475928859726992,
      "judge_s": 0.6475928859726992,
      "luna_s": null,
      "total_s": 0.6475947959697805,
      "writer_s": 1.9099970813840628e-06
    }
  },
  {
    "case_id": "U16-e12",
    "record": {
      "comment_id": "U16-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 2135,
            "latency_s": 0.597005,
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
                "guess": 0.08,
                "question": 0.92
              },
              "A2": {
                "q_multi": 0.72,
                "q_open": 0.01,
                "q_yesno": 0.27
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
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "1 つずつ聞いてくれたら、ちゃんと答えるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "女は助けに来た人なの？それとも男と一緒にいた人？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.5971733760088682,
      "judge_s": 0.5971733760088682,
      "luna_s": null,
      "total_s": 0.5971750910102855,
      "writer_s": 1.715001417323947e-06
    }
  },
  {
    "case_id": "U16-e13",
    "record": {
      "comment_id": "U16-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 2646,
            "latency_s": 0.788104,
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
                "q_open": 0.99,
                "q_yesno": 0.01
              },
              "A3": 0.03,
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.03"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい か いいえ で答えられる質問にしてごらん🤔"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "助けに来た女まで動けなくなったのはなぜ？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.7883306439907756,
      "judge_s": 0.7883306439907756,
      "luna_s": null,
      "total_s": 0.7883320380060468,
      "writer_s": 1.394015271216631e-06
    }
  },
  {
    "case_id": "U16-e14",
    "record": {
      "comment_id": "U16-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 2126,
            "latency_s": 0.673675,
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
                "q_multi": 0.9,
                "q_open": 0.1,
                "q_yesno": 0.0
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
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "ひとつずつなら答えられるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "二人はどこで、何をしている最中なんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.6738219060061965,
      "judge_s": 0.6738219060061965,
      "luna_s": null,
      "total_s": 0.67382356399321,
      "writer_s": 1.6579870134592056e-06
    }
  },
  {
    "case_id": "U16-e15",
    "record": {
      "comment_id": "U16-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 2646,
            "latency_s": 0.791934,
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
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい・いいえで答えられる形で聞き直してね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "誰が男を助けようとしていたんでしょうか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.7921553859778214,
      "judge_s": 0.7921553859778214,
      "luna_s": null,
      "total_s": 0.7921898599888664,
      "writer_s": 3.447401104494929e-05
    }
  },
  {
    "case_id": "U16-e16",
    "record": {
      "comment_id": "U16-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "calls": 3,
            "input_tokens": 1967,
            "latency_s": 0.597151,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 132,
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
                "point_0": 0.78
              }
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.78"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！2人は子どもと氷鬼をしていた。男は鬼にタッチされて凍り、助けに来た女も男に触れる直前にタッチされて凍った。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "夫婦で子どもたちと氷鬼をしてたってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.5973549699992873,
      "judge_s": 0.5973549699992873,
      "luna_s": null,
      "total_s": 0.5973564529849682,
      "writer_s": 1.4829856809228659e-06
    }
  },
  {
    "case_id": "U16-e17",
    "record": {
      "comment_id": "U16-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "calls": 3,
            "input_tokens": 2048,
            "latency_s": 0.801646,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 132,
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
                "point_0": 0.91
              }
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.91"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！2人は子どもと氷鬼をしていた。男は鬼にタッチされて凍り、助けに来た女も男に触れる直前にタッチされて凍った。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "夫婦で子どもたちと氷鬼をしてたんだね。男も女も鬼にタッチされて、その場で凍ってしまったのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.8019096210191492,
      "judge_s": 0.8019096210191492,
      "luna_s": null,
      "total_s": 0.8019105920102447,
      "writer_s": 9.709910955280066e-07
    }
  },
  {
    "case_id": "U16-e18",
    "record": {
      "comment_id": "U16-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 4264,
            "latency_s": 1.201047,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
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
                "q_multi": 0.0,
                "q_open": 0.07,
                "q_yesno": 0.93
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.04
              },
              "C": 0.35,
              "D": {
                "irrelevant": 0.01,
                "no": 0.02,
                "yes": 0.97
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.04"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい！まだまだ聞いていいんだよ😌"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "子どもたちと鬼ごっこをしてたんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2014597649977077,
      "judge_s": 1.2014597649977077,
      "luna_s": null,
      "total_s": 1.2014616139931604,
      "writer_s": 1.848995452746749e-06
    }
  },
  {
    "case_id": "U16-e19",
    "record": {
      "comment_id": "U16-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "calls": 3,
            "input_tokens": 2063,
            "latency_s": 0.592147,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 132,
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
                "point_0": 0.93
              }
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.93"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！2人は子どもと氷鬼をしていた。男は鬼にタッチされて凍り、助けに来た女も男に触れる直前にタッチされて凍った。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "夫婦で子どもたちと氷鬼をしてたんだね。でも女は助けに来たふりで、実は鬼側に回って男を置き去りにしたのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.5923428520036396,
      "judge_s": 0.5923428520036396,
      "luna_s": null,
      "total_s": 0.5923438730242196,
      "writer_s": 1.0210205800831318e-06
    }
  },
  {
    "case_id": "U16-e20",
    "record": {
      "comment_id": "U16-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 4360,
            "latency_s": 1.268085,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
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
                "q_open": 0.06,
                "q_yesno": 0.92
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.17
              },
              "C": 0.28,
              "D": {
                "irrelevant": 0.0,
                "no": 1.0,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.17"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "いいえ。なるほど、メモしておくね🧐"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "二人とも吹雪で遭難して、助けを待ってるうちに凍えてしまったんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2683859549870249,
      "judge_s": 1.2683859549870249,
      "luna_s": null,
      "total_s": 1.2683875379734673,
      "writer_s": 1.5829864423722029e-06
    }
  },
  {
    "case_id": "U16-e21",
    "record": {
      "comment_id": "U16-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 2006,
            "latency_s": 0.574627,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 132,
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
                "point_0": 0.45
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.45"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "惜しい！質問で確かめてみるといいよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は氷の彫刻で、女も作品を見た瞬間に固まってしまったんだと思う。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.5748333600058686,
      "judge_s": 0.5748333600058686,
      "luna_s": null,
      "total_s": 0.57483527000295,
      "writer_s": 1.9099970813840628e-06
    }
  },
  {
    "case_id": "U16-t01",
    "record": {
      "comment_id": "U16-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "氷鬼",
          "debug": {
            "calls": 1,
            "input_tokens": 928,
            "latency_s": 0.211976,
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
              "A_bare": 0.88
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.88"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "氷鬼がどうしたのか聞かせてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "氷鬼？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.21210576099110767,
      "judge_s": 0.21210576099110767,
      "luna_s": null,
      "total_s": 0.2121081340010278,
      "writer_s": 2.3730099201202393e-06
    }
  },
  {
    "case_id": "U16-t02",
    "record": {
      "comment_id": "U16-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "傘",
          "debug": {
            "calls": 1,
            "input_tokens": 926,
            "latency_s": 0.209809,
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
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "傘が何のことか、もう少し詳しく教えて！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "傘",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.20991785000660457,
      "judge_s": 0.20991785000660457,
      "luna_s": null,
      "total_s": 0.209919967019232,
      "writer_s": 2.1170126274228096e-06
    }
  },
  {
    "case_id": "c-ask_hint-05",
    "record": {
      "comment_id": "c-ask_hint-05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "ask_hint"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1427,
            "latency_s": 0.407013,
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
              "A_bare": 0.1
            }
          },
          "error": null,
          "kind": "ask_hint",
          "reason": "段A=request→ask_hint"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい・いいえで聞いて、自分で見つけてごらん🧐"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "もう一声ヒントお願い！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.40710339599172585,
      "judge_s": 0.40710339599172585,
      "luna_s": null,
      "total_s": 0.4071082150039729,
      "writer_s": 4.819012247025967e-06
    }
  },
  {
    "case_id": "c-impression-04",
    "record": {
      "comment_id": "c-impression-04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "impression"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1594,
            "latency_s": 0.474876,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 150,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.02,
                "reaction": 0.98,
                "request": 0.0
              },
              "A2": {
                "chat": 0.0,
                "cheer": 0.0,
                "complaint": 0.02,
                "greeting": 0.0,
                "impression": 0.98,
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
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "ありがとう！また遊びにおいで。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "うーん、なんかモヤモヤするね",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.47509542998159304,
      "judge_s": 0.47509542998159304,
      "luna_s": null,
      "total_s": 0.4751004699792247,
      "writer_s": 5.039997631683946e-06
    }
  },
  {
    "case_id": "c-chat-03",
    "record": {
      "comment_id": "c-chat-03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "chat"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1582,
            "latency_s": 0.443508,
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
              "A_bare": 0.06
            }
          },
          "error": null,
          "kind": "chat",
          "reason": "段A=reaction→chat"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "ふむふむ、そうなんだね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "お腹すいてきた笑",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.4436231550062075,
      "judge_s": 0.4436231550062075,
      "luna_s": null,
      "total_s": 0.4436279680230655,
      "writer_s": 4.8130168579518795e-06
    }
  },
  {
    "case_id": "c-mention-02",
    "record": {
      "comment_id": "c-mention-02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "mention"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1588,
            "latency_s": 0.408833,
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
                "chat": 0.04,
                "cheer": 0.01,
                "complaint": 0.01,
                "greeting": 0.0,
                "impression": 0.01,
                "mention": 0.93,
                "request": 0.0
              },
              "A_bare": 0.06
            }
          },
          "error": null,
          "kind": "mention",
          "reason": "段A=reaction→mention"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "ふたりで考えてみてね😉"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "@tomo また出てるよ〜",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.40892245300346985,
      "judge_s": 0.40892245300346985,
      "luna_s": null,
      "total_s": 0.4089267490198836,
      "writer_s": 4.296016413718462e-06
    }
  },
  {
    "case_id": "c-complaint-06",
    "record": {
      "comment_id": "c-complaint-06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
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
            "input_tokens": 1586,
            "latency_s": 0.418151,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 149,
            "probabilities": {
              "A1": {
                "inappropriate": 0.16,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.84,
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
              "A_bare": 0.32
            }
          },
          "error": null,
          "kind": "complaint",
          "reason": "段A=reaction→complaint"
        },
        "luna": null
      },
      "media_id": "local-U16",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "ありがとう。確認するね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "つまらん、センスない",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.41832671902375296,
      "judge_s": 0.41832671902375296,
      "luna_s": null,
      "total_s": 0.41833129202132113,
      "writer_s": 4.572997568175197e-06
    }
  },
  {
    "case_id": "c-personal_info-05",
    "record": {
      "comment_id": "c-personal_info-05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "006-frozen-tag",
      "errors": [],
      "fact_sheet_hash": "574fa29e940c",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "personal_info"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1506,
            "latency_s": 0.449772,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
            "probabilities": {
              "A1": {
                "inappropriate": 0.98,
                "other": 0.0,
                "question_or_guess": 0.01,
                "reaction": 0.01,
                "request": 0.0
              },
              "A2": {
                "abuse": 0.0,
                "personal_info": 0.92,
                "spam": 0.0,
                "troll": 0.08
              },
              "A_bare": 0.12
            }
          },
          "error": null,
          "kind": "personal_info",
          "reason": "段A=inappropriate→personal_info"
        },
        "luna": null
      },
      "media_id": "local-U16",
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
      "text": "〒000-0000 東京都架空市テスト町1-2-3です",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.44990167798823677,
      "judge_s": 0.44990167798823677,
      "luna_s": null,
      "total_s": 0.4499040379887447,
      "writer_s": 2.3600005079060793e-06
    }
  }
];
