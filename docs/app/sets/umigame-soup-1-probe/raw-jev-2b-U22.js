window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["jev-2b/U22"] = [
  {
    "case_id": "U22-e01",
    "record": {
      "comment_id": "U22-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4241,
            "latency_s": 1.263779,
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
                "guess": 0.61,
                "question": 0.39
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              },
              "C": 0.58,
              "D": {
                "irrelevant": 0.0,
                "no": 0.03,
                "yes": 0.97
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": null
      },
      "media_id": "local-U22",
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
      "text": "男は半年ごとに定期検診を受けてるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2640964790189173,
      "judge_s": 1.2640964790189173,
      "luna_s": null,
      "total_s": 1.2640989250212442,
      "writer_s": 2.4460023269057274e-06
    }
  },
  {
    "case_id": "U22-e02",
    "record": {
      "comment_id": "U22-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4277,
            "latency_s": 1.112357,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.01,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.18,
                "question": 0.82
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.04,
                "q_yesno": 0.96
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              },
              "C": 0.43,
              "D": {
                "irrelevant": 0.0,
                "no": 0.99,
                "yes": 0.01
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "いいえ。じっくり考えてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "歯医者に通うのは、歯の治療が目的じゃないんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1128271539928392,
      "judge_s": 1.1128271539928392,
      "luna_s": null,
      "total_s": 1.112829512974713,
      "writer_s": 2.3589818738400936e-06
    }
  },
  {
    "case_id": "U22-e03",
    "record": {
      "comment_id": "U22-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4247,
            "latency_s": 1.140433,
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
                "point_0": 0.1
              },
              "C": 0.34,
              "D": {
                "irrelevant": 0.01,
                "no": 0.97,
                "yes": 0.02
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.10"
        },
        "luna": null
      },
      "media_id": "local-U22",
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
      "text": "その歯医者は男の昔からのかかりつけですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1409050070215017,
      "judge_s": 1.1409050070215017,
      "luna_s": null,
      "total_s": 1.140907559019979,
      "writer_s": 2.5519984774291515e-06
    }
  },
  {
    "case_id": "U22-e04",
    "record": {
      "comment_id": "U22-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4259,
            "latency_s": 1.190091,
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
                "guess": 0.88,
                "question": 0.12
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              },
              "C": 0.67,
              "D": {
                "irrelevant": 0.01,
                "no": 0.99,
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
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "いいえ。じっくり考えてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は診察のあと誰かが来るのを待っているんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1904580749978777,
      "judge_s": 1.1904580749978777,
      "luna_s": null,
      "total_s": 1.1904605860181618,
      "writer_s": 2.5110202841460705e-06
    }
  },
  {
    "case_id": "U22-e05",
    "record": {
      "comment_id": "U22-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4229,
            "latency_s": 1.235977,
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
                "guess": 0.02,
                "question": 0.98
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.07,
                "q_yesno": 0.93
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.01
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
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": null
      },
      "media_id": "local-U22",
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
      "text": "同じ席に座ることに意味があるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2362973330018576,
      "judge_s": 1.2362973330018576,
      "luna_s": null,
      "total_s": 1.236300285992911,
      "writer_s": 2.9529910534620285e-06
    }
  },
  {
    "case_id": "U22-e06",
    "record": {
      "comment_id": "U22-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": "irrelevant",
        "decision": "jev",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4253,
            "latency_s": 1.230426,
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
                "guess": 0.47,
                "question": 0.53
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02
              },
              "C": 0.58,
              "D": {
                "irrelevant": 0.38,
                "no": 0.39999999999999997,
                "yes": 0.22
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "関係ないよ。ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は毎回、歯医者の人と話をして帰るんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2307011839875486,
      "judge_s": 1.2307011839875486,
      "luna_s": null,
      "total_s": 1.2307043969922233,
      "writer_s": 3.2130046747624874e-06
    }
  },
  {
    "case_id": "U22-e07",
    "record": {
      "comment_id": "U22-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4223,
            "latency_s": 1.239964,
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
                "guess": 0.42,
                "question": 0.58
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.01
              },
              "C": 0.27,
              "D": {
                "irrelevant": 0.42,
                "no": 0.57,
                "yes": 0.01
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": null
      },
      "media_id": "local-U22",
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
      "text": "その町に家族や友人が住んでいますか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2403570429887623,
      "judge_s": 1.2403570429887623,
      "luna_s": null,
      "total_s": 1.2403594179777429,
      "writer_s": 2.374988980591297e-06
    }
  },
  {
    "case_id": "U22-e08",
    "record": {
      "comment_id": "U22-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": "irrelevant",
        "decision": "jev",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4295,
            "latency_s": 1.234048,
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
                "guess": 0.02,
                "question": 0.98
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.25,
                "q_yesno": 0.74
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              },
              "C": 0.41,
              "D": {
                "irrelevant": 0.25,
                "no": 0.39999999999999997,
                "yes": 0.35
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "関係ないよ。まだまだ聞いていいんだよ😌"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "歯医者に行くのは電車じゃないといけない理由があるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2343748240091372,
      "judge_s": 1.2343748240091372,
      "luna_s": null,
      "total_s": 1.2343775540066417,
      "writer_s": 2.729997504502535e-06
    }
  },
  {
    "case_id": "U22-e09",
    "record": {
      "comment_id": "U22-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": "irrelevant",
        "decision": "jev",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4253,
            "latency_s": 1.252263,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 240,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.33,
                "question": 0.67
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              },
              "C": 0.44,
              "D": {
                "irrelevant": 0.76,
                "no": 0.16,
                "yes": 0.08
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "関係ないよ。さあ、次はなにを聞く？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "待合室にいる時間のほうが診察より長いんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2530309229914565,
      "judge_s": 1.2530309229914565,
      "luna_s": null,
      "total_s": 1.2530334859911818,
      "writer_s": 2.562999725341797e-06
    }
  },
  {
    "case_id": "U22-e10",
    "record": {
      "comment_id": "U22-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4211,
            "latency_s": 1.364204,
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
                "guess": 0.13,
                "question": 0.87
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
              "C": 0.23,
              "D": {
                "irrelevant": 0.15,
                "no": 0.02,
                "yes": 0.83
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい！なるほど、メモしておくね🧐"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "その歯医者の建物は木造ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.3646090020192787,
      "judge_s": 1.3646090020192787,
      "luna_s": null,
      "total_s": 1.3646114919974934,
      "writer_s": 2.489978214725852e-06
    }
  },
  {
    "case_id": "U22-e11",
    "record": {
      "comment_id": "U22-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 2145,
            "latency_s": 0.576117,
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
                "guess": 0.44,
                "question": 0.56
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
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "1 コメントに 1 つの質問でお願いね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は歯の検診に来てるの？診察後は誰かを待ってるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.5763122149801347,
      "judge_s": 0.5763122149801347,
      "luna_s": null,
      "total_s": 0.5763161899812985,
      "writer_s": 3.975001163780689e-06
    }
  },
  {
    "case_id": "U22-e12",
    "record": {
      "comment_id": "U22-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 2145,
            "latency_s": 0.596307,
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
                "guess": 0.72,
                "question": 0.28
              },
              "A2": {
                "q_multi": 0.96,
                "q_open": 0.03,
                "q_yesno": 0.01
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
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "質問は 1 つずつコメントしてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "同じ席に座るのは昔から？その席に何か思い出があるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.5964398670184892,
      "judge_s": 0.5964398670184892,
      "luna_s": null,
      "total_s": 0.5964424539997708,
      "writer_s": 2.5869812816381454e-06
    }
  },
  {
    "case_id": "U22-e13",
    "record": {
      "comment_id": "U22-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 2670,
            "latency_s": 0.800928,
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
                "guess": 0.16,
                "question": 0.84
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
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい・いいえで答えられるように、もう一度聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男はどうして遠くの歯医者に通ってるんでしょう？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.8011045180028304,
      "judge_s": 0.8011045180028304,
      "luna_s": null,
      "total_s": 0.8011068310006522,
      "writer_s": 2.3129978217184544e-06
    }
  },
  {
    "case_id": "U22-e14",
    "record": {
      "comment_id": "U22-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 2678,
            "latency_s": 0.751913,
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
                "guess": 0.16,
                "question": 0.84
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.98,
                "q_yesno": 0.02
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
      "media_id": "local-U22",
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
      "text": "診察が終わったあと、待合室で誰を待っているんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.752073472016491,
      "judge_s": 0.752073472016491,
      "luna_s": null,
      "total_s": 0.7520761460182257,
      "writer_s": 2.6740017347037792e-06
    }
  },
  {
    "case_id": "U22-e15",
    "record": {
      "comment_id": "U22-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 2674,
            "latency_s": 0.766429,
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
                "q_multi": 0.03,
                "q_open": 0.96,
                "q_yesno": 0.01
              },
              "A3": 0.07,
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.07"
        },
        "luna": null
      },
      "media_id": "local-U22",
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
      "text": "その町や歯医者と男にはどんな関係があるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7666856730065774,
      "judge_s": 0.7666856730065774,
      "luna_s": null,
      "total_s": 0.7666881819895934,
      "writer_s": 2.508983016014099e-06
    }
  },
  {
    "case_id": "U22-e16",
    "record": {
      "comment_id": "U22-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 3230,
            "latency_s": 1.04582,
            "major": "guess",
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
                "guess": 0.95,
                "question": 0.05
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.9
              },
              "B2": 0.24
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.90, 矛盾=0.24"
        },
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！その歯医者は男が育った家を改装したもの。男は検診を口実に通い、背丈の傷が残る柱の前で過ごしてから帰る。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "歯医者は男が子どものころ住んでた家だったってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.0461228149943054,
      "judge_s": 1.0461228149943054,
      "luna_s": null,
      "total_s": 1.0461250259832013,
      "writer_s": 2.2109888959676027e-06
    }
  },
  {
    "case_id": "U22-e17",
    "record": {
      "comment_id": "U22-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 3342,
            "latency_s": 0.811118,
            "major": "guess",
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
                "guess": 1.0,
                "question": 0.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.93
              },
              "B2": 0.12
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.93, 矛盾=0.12"
        },
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！その歯医者は男が育った家を改装したもの。男は検診を口実に通い、背丈の傷が残る柱の前で過ごしてから帰る。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "歯医者になっていたのは男が育った家なんだね。懐かしい家の中に入るために、検診のたび待合室に残ってたのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.8113807500049006,
      "judge_s": 0.8113807500049006,
      "luna_s": null,
      "total_s": 0.8113826610206161,
      "writer_s": 1.9110157154500484e-06
    }
  },
  {
    "case_id": "U22-e18",
    "record": {
      "comment_id": "U22-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4301,
            "latency_s": 1.284581,
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
                "guess": 0.99,
                "question": 0.01
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.04,
                "q_yesno": 0.96
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.12
              },
              "C": 0.3,
              "D": {
                "irrelevant": 0.0,
                "no": 0.0,
                "yes": 1.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.12"
        },
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい！なるほど、メモしておくね🧐"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "その歯医者の建物って、男が昔なにか関わってた場所なんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.284962251986144,
      "judge_s": 1.284962251986144,
      "luna_s": null,
      "total_s": 1.2849651629803702,
      "writer_s": 2.9109942261129618e-06
    }
  },
  {
    "case_id": "U22-e19",
    "record": {
      "comment_id": "U22-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 3366,
            "latency_s": 0.791854,
            "major": "guess",
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
                "guess": 0.99,
                "question": 0.01
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.94
              },
              "B2": 0.89
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.94, 矛盾=0.89"
        },
        "luna": null
      },
      "media_id": "local-U22",
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
      "text": "歯医者は男が育った家で、待合室の柱の傷も残ってたんだね。あの背丈の傷は父親じゃなくて、歯医者を開いた人が刻んだのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7920360759890173,
      "judge_s": 0.7920360759890173,
      "luna_s": null,
      "total_s": 0.7920385109900963,
      "writer_s": 2.435001078993082e-06
    }
  },
  {
    "case_id": "U22-e20",
    "record": {
      "comment_id": "U22-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4331,
            "latency_s": 1.188275,
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
                "q_multi": 0.01,
                "q_open": 0.08,
                "q_yesno": 0.91
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02
              },
              "C": 0.47,
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
      "media_id": "local-U22",
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
      "text": "昔から通ってる先生に会いたくて、診察を口実に半年ごとに訪ねてるんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1885067349940073,
      "judge_s": 1.1885067349940073,
      "luna_s": null,
      "total_s": 1.188509047991829,
      "writer_s": 2.3129978217184544e-06
    }
  },
  {
    "case_id": "U22-e21",
    "record": {
      "comment_id": "U22-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 2547,
            "latency_s": 0.756715,
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
                "guess": 1.0,
                "question": 0.0
              },
              "A2": {
                "q_multi": 0.02,
                "q_open": 0.76,
                "q_yesno": 0.22
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.01
              }
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.01"
        },
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "ざんねん、ちがうんだ🫢"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "待合室の席に忘れ物をしていて、診察のたびに探してるんだと思う。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7569146369933151,
      "judge_s": 0.7569146369933151,
      "luna_s": null,
      "total_s": 0.7569170059869066,
      "writer_s": 2.36899359151721e-06
    }
  },
  {
    "case_id": "U22-t01",
    "record": {
      "comment_id": "U22-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "生家の歯医者",
          "debug": {
            "calls": 1,
            "input_tokens": 932,
            "latency_s": 0.195487,
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
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "生家の歯医者がどうしたのか聞かせてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "生家の歯医者？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.19555302397930063,
      "judge_s": 0.19555302397930063,
      "luna_s": null,
      "total_s": 0.1955558320041746,
      "writer_s": 2.808024873957038e-06
    }
  },
  {
    "case_id": "U22-t02",
    "record": {
      "comment_id": "U22-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "引っ越し",
          "debug": {
            "calls": 1,
            "input_tokens": 928,
            "latency_s": 0.192886,
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
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "引っ越しが何のことか、もう少し詳しく教えて！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "引っ越し",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.1929395140032284,
      "judge_s": 0.1929395140032284,
      "luna_s": null,
      "total_s": 0.19294225401245058,
      "writer_s": 2.7400092221796513e-06
    }
  },
  {
    "case_id": "c-ask_spoiler-04",
    "record": {
      "comment_id": "c-ask_spoiler-04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "ask_spoiler"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1419,
            "latency_s": 0.423795,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 124,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.08,
                "reaction": 0.0,
                "request": 0.92
              },
              "A2": {
                "ask_hint": 0.0,
                "ask_howto": 0.0,
                "ask_spoiler": 1.0
              },
              "A_bare": 0.1
            }
          },
          "error": null,
          "kind": "ask_spoiler",
          "reason": "段A=request→ask_spoiler"
        },
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "質問には答えられるけど、真相は教えられないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "正解は何なん？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.42391502900864,
      "judge_s": 0.42391502900864,
      "luna_s": null,
      "total_s": 0.42391833700821735,
      "writer_s": 3.3079995773732662e-06
    }
  },
  {
    "case_id": "c-greeting-03",
    "record": {
      "comment_id": "c-greeting-03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "greeting"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1576,
            "latency_s": 0.356107,
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
              "A_bare": 0.55
            }
          },
          "error": null,
          "kind": "greeting",
          "reason": "段A=reaction→greeting"
        },
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "やあ！今日もよろしくね🙌"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "こんちは！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.35618578898720443,
      "judge_s": 0.35618578898720443,
      "luna_s": null,
      "total_s": 0.3561885829840321,
      "writer_s": 2.7939968276768923e-06
    }
  },
  {
    "case_id": "c-request-02",
    "record": {
      "comment_id": "c-request-02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "request"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1588,
            "latency_s": 0.369296,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 148,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.04,
                "reaction": 0.8,
                "request": 0.16
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
              "A_bare": 0.3
            }
          },
          "error": null,
          "kind": "request",
          "reason": "段A=reaction→request"
        },
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "リクエストうれしいな。参考にするよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "動物が出てくるやつ希望",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.3694055679952726,
      "judge_s": 0.3694055679952726,
      "luna_s": null,
      "total_s": 0.36940805197809823,
      "writer_s": 2.483982825651765e-06
    }
  },
  {
    "case_id": "c-emoji_only-01",
    "record": {
      "comment_id": "c-emoji_only-01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": null,
        "decision": "jev",
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
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "受け取ったよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "🤔💭",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 6.247599958442152e-05,
      "judge_s": 6.247599958442152e-05,
      "luna_s": null,
      "total_s": 6.555800791829824e-05,
      "writer_s": 3.082008333876729e-06
    }
  },
  {
    "case_id": "c-abuse-05",
    "record": {
      "comment_id": "c-abuse-05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "abuse"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1486,
            "latency_s": 0.382243,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
            "probabilities": {
              "A1": {
                "inappropriate": 0.91,
                "other": 0.0,
                "question_or_guess": 0.01,
                "reaction": 0.08,
                "request": 0.0
              },
              "A2": {
                "abuse": 1.0,
                "personal_info": 0.0,
                "spam": 0.0,
                "troll": 0.0
              },
              "A_bare": 0.04
            }
          },
          "error": null,
          "kind": "abuse",
          "reason": "段A=inappropriate→abuse"
        },
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "ここではやさしい言葉でお願いね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "性的なことばっか考えてそうでキモい",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.38237115999800153,
      "judge_s": 0.38237115999800153,
      "luna_s": null,
      "total_s": 0.3823739429935813,
      "writer_s": 2.782995579764247e-06
    }
  },
  {
    "case_id": "c-foreign-04",
    "record": {
      "comment_id": "c-foreign-04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "ask_spoiler"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1417,
            "latency_s": 0.378275,
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
                "ask_howto": 0.0,
                "ask_spoiler": 1.0
              },
              "A_bare": 0.13
            }
          },
          "error": null,
          "kind": "ask_spoiler",
          "reason": "段A=request→ask_spoiler"
        },
        "luna": null
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "それは教えられないんだ。質問には答えるからね😉"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "答案是什么？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.3784328470064793,
      "judge_s": 0.3784328470064793,
      "luna_s": null,
      "total_s": 0.3784359130077064,
      "writer_s": 3.0660012271255255e-06
    }
  }
];
