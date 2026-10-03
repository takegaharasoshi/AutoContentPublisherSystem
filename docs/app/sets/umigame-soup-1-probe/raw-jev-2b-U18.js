window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["jev-2b/U18"] = [
  {
    "case_id": "U18-e01",
    "record": {
      "comment_id": "U18-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4067,
            "latency_s": 1.149158,
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
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.03,
                "point_1": 0.02
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
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "いいえ。さあ、次はなにを聞く？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "約束は口約束だったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.149552495975513,
      "judge_s": 1.149552495975513,
      "luna_s": null,
      "total_s": 1.1495578289905097,
      "writer_s": 5.333014996722341e-06
    }
  },
  {
    "case_id": "U18-e02",
    "record": {
      "comment_id": "U18-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4103,
            "latency_s": 1.191551,
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
              "A_bare": 0.04,
              "B": {
                "point_0": 0.25,
                "point_1": 0.07
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
          "reason": "段A=question→q_yesno, 要点最低=0.07"
        },
        "luna": null
      },
      "media_id": "local-U18",
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
      "text": "白紙になったのは、目に見えるもの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1920290129783098,
      "judge_s": 1.1920290129783098,
      "luna_s": null,
      "total_s": 1.1920321049983613,
      "writer_s": 3.0920200515538454e-06
    }
  },
  {
    "case_id": "U18-e03",
    "record": {
      "comment_id": "U18-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4067,
            "latency_s": 1.21243,
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
                "guess": 0.85,
                "question": 0.15
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
        "luna": null
      },
      "media_id": "local-U18",
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
      "text": "ふたりはけんかしてた？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2127657079836354,
      "judge_s": 1.2127657079836354,
      "luna_s": null,
      "total_s": 1.2127693079819437,
      "writer_s": 3.5999983083456755e-06
    }
  },
  {
    "case_id": "U18-e04",
    "record": {
      "comment_id": "U18-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4067,
            "latency_s": 1.222262,
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
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.07,
              "B": {
                "point_0": 0.03,
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
        "luna": null
      },
      "media_id": "local-U18",
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
      "text": "夏の夕立が関係してる？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2226510549953673,
      "judge_s": 1.2226510549953673,
      "luna_s": null,
      "total_s": 1.2226538980030455,
      "writer_s": 2.843007678166032e-06
    }
  },
  {
    "case_id": "U18-e05",
    "record": {
      "comment_id": "U18-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4079,
            "latency_s": 1.113848,
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
              "A_bare": 0.03,
              "B": {
                "point_0": 0.03,
                "point_1": 0.04
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
          "reason": "段A=question→q_yesno, 要点最低=0.03"
        },
        "luna": null
      },
      "media_id": "local-U18",
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
      "text": "濡れたものを乾かしたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1142112980014645,
      "judge_s": 1.1142112980014645,
      "luna_s": null,
      "total_s": 1.1142143119941466,
      "writer_s": 3.0139926820993423e-06
    }
  },
  {
    "case_id": "U18-e06",
    "record": {
      "comment_id": "U18-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4079,
            "latency_s": 1.253131,
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
                "guess": 0.93,
                "question": 0.07
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
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "いいえ。ひとつずつ確かめていこうね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "約束そのものを取り消した？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2534947759995703,
      "judge_s": 1.2534947759995703,
      "luna_s": null,
      "total_s": 1.2534975760208908,
      "writer_s": 2.800021320581436e-06
    }
  },
  {
    "case_id": "U18-e07",
    "record": {
      "comment_id": "U18-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4091,
            "latency_s": 1.261152,
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
                "q_open": 0.01,
                "q_yesno": 0.98
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.02,
                "point_1": 0.01
              },
              "C": 0.36,
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
      "media_id": "local-U18",
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
      "text": "約束の中身は二人とも覚えてた？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2614649360184558,
      "judge_s": 1.2614649360184558,
      "luna_s": null,
      "total_s": 1.261467870004708,
      "writer_s": 2.9339862521737814e-06
    }
  },
  {
    "case_id": "U18-e08",
    "record": {
      "comment_id": "U18-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4067,
            "latency_s": 1.304226,
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
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.07,
              "B": {
                "point_0": 0.03,
                "point_1": 0.02
              },
              "C": 0.32,
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
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "いいえ。ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "誰かのいたずらだった？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.30457381598535,
      "judge_s": 1.30457381598535,
      "luna_s": null,
      "total_s": 1.304577448987402,
      "writer_s": 3.6330020520836115e-06
    }
  },
  {
    "case_id": "U18-e09",
    "record": {
      "comment_id": "U18-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4091,
            "latency_s": 1.185162,
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
                "guess": 0.07,
                "question": 0.93
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
              "C": 0.81,
              "D": {
                "irrelevant": 0.02,
                "no": 0.0,
                "yes": 0.98
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい！じっくり考えてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "二人は後日その約束を果たした？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.185468211013358,
      "judge_s": 1.185468211013358,
      "luna_s": null,
      "total_s": 1.1854758039989974,
      "writer_s": 7.592985639348626e-06
    }
  },
  {
    "case_id": "U18-e10",
    "record": {
      "comment_id": "U18-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4115,
            "latency_s": 1.315624,
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
        "luna": null
      },
      "media_id": "local-U18",
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
      "text": "二人の年齢って謎を解くのに関係ある？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.3159668410080485,
      "judge_s": 1.3159668410080485,
      "luna_s": null,
      "total_s": 1.3159709570172708,
      "writer_s": 4.116009222343564e-06
    }
  },
  {
    "case_id": "U18-e11",
    "record": {
      "comment_id": "U18-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2122,
            "latency_s": 0.637719,
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
                "guess": 0.64,
                "question": 0.36
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
        "luna": null
      },
      "media_id": "local-U18",
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
      "text": "雨で何か濡れたの？そのあとどうしたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.6378967490163632,
      "judge_s": 0.6378967490163632,
      "luna_s": null,
      "total_s": 0.6379003840265796,
      "writer_s": 3.635010216385126e-06
    }
  },
  {
    "case_id": "U18-e12",
    "record": {
      "comment_id": "U18-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2143,
            "latency_s": 0.65191,
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
        "luna": null
      },
      "media_id": "local-U18",
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
      "text": "約束は取り消されたの？それでも二人はあとで実行したの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.6520894609857351,
      "judge_s": 0.6520894609857351,
      "luna_s": null,
      "total_s": 0.6520930289989337,
      "writer_s": 3.568013198673725e-06
    }
  },
  {
    "case_id": "U18-e13",
    "record": {
      "comment_id": "U18-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2668,
            "latency_s": 0.784052,
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
      "media_id": "local-U18",
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
      "text": "なぜ約束が白紙に戻ったのに、二人は悲しまなかったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7842932009953074,
      "judge_s": 0.7842932009953074,
      "luna_s": null,
      "total_s": 0.78430072098854,
      "writer_s": 7.519993232563138e-06
    }
  },
  {
    "case_id": "U18-e14",
    "record": {
      "comment_id": "U18-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2632,
            "latency_s": 0.743733,
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
                "q_open": 1.0,
                "q_yesno": 0.0
              },
              "A3": 0.04,
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.04"
        },
        "luna": null
      },
      "media_id": "local-U18",
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
      "text": "どうして後日その約束を果たせたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7441035810043104,
      "judge_s": 0.7441035810043104,
      "luna_s": null,
      "total_s": 0.7441087170154788,
      "writer_s": 5.13601116836071e-06
    }
  },
  {
    "case_id": "U18-e15",
    "record": {
      "comment_id": "U18-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2608,
            "latency_s": 1.027383,
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
                "guess": 0.23,
                "question": 0.77
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.22,
                "q_yesno": 0.78
              },
              "A3": 0.39,
              "A_bare": 0.03
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.39"
        },
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "その聞き方だと答えにくいな。はい・いいえで聞いてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "それはまだ覚えてるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.0276265630091075,
      "judge_s": 1.0276265630091075,
      "luna_s": null,
      "total_s": 1.0276312560017686,
      "writer_s": 4.69299266114831e-06
    }
  },
  {
    "case_id": "U18-e16",
    "record": {
      "comment_id": "U18-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 3325,
            "latency_s": 0.891758,
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
                "point_0": 0.97,
                "point_1": 0.98
              },
              "B2": 0.05
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.97, 矛盾=0.05"
        },
        "luna": null
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
      "shadow_mismatch": null,
      "text": "男が消せるボールペンで書いた手紙が夕立で濡れ、女がドライヤーで乾かした熱で文字が消えて白紙になった。二人は約束の中身を覚えていて書き直し、後日果たした。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.8920870659931097,
      "judge_s": 0.8920870659931097,
      "luna_s": null,
      "total_s": 0.8920900810044259,
      "writer_s": 3.015011316165328e-06
    }
  },
  {
    "case_id": "U18-e17",
    "record": {
      "comment_id": "U18-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 3289,
            "latency_s": 0.746755,
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
                "point_0": 0.95,
                "point_1": 0.97
              },
              "B2": 0.08
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.95, 矛盾=0.08"
        },
        "luna": null
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
      "shadow_mismatch": null,
      "text": "夕立で濡れた手紙をドライヤーで乾かしたら、消せるペンの文字が熱で消えた。でも二人とも約束は覚えていて、書き直して後日果たしたってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7469880360004026,
      "judge_s": 0.7469880360004026,
      "luna_s": null,
      "total_s": 0.7469921979936771,
      "writer_s": 4.161993274465203e-06
    }
  },
  {
    "case_id": "U18-e18",
    "record": {
      "comment_id": "U18-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2121,
            "latency_s": 0.600166,
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
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "惜しい！もうひと押しだよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "雨に濡れた紙の文字が消えて白紙になったけど、二人は約束の内容を覚えていたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.6004157350107562,
      "judge_s": 0.6004157350107562,
      "luna_s": null,
      "total_s": 0.600421234004898,
      "writer_s": 5.498994141817093e-06
    }
  },
  {
    "case_id": "U18-e19",
    "record": {
      "comment_id": "U18-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2109,
            "latency_s": 0.60446,
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
                "point_0": 0.88,
                "point_1": 0.17
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.17"
        },
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "惜しい！もう少し考えてみようか🤔"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "約束は紙に書かれていて、白紙になったあと二人は同じ約束を続けたんじゃない？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.604652937996434,
      "judge_s": 0.604652937996434,
      "luna_s": null,
      "total_s": 0.6046559560054448,
      "writer_s": 3.0180090107023716e-06
    }
  },
  {
    "case_id": "U18-e20",
    "record": {
      "comment_id": "U18-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2646,
            "latency_s": 0.869379,
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
                "q_open": 0.62,
                "q_yesno": 0.34
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
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "残念、そうじゃないんだ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "二人が大げんかして約束を取り消し、仲直りしたあと別の約束をしたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.8695580460189376,
      "judge_s": 0.8695580460189376,
      "luna_s": null,
      "total_s": 0.8695619600184727,
      "writer_s": 3.913999535143375e-06
    }
  },
  {
    "case_id": "U18-e21",
    "record": {
      "comment_id": "U18-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 2658,
            "latency_s": 0.75278,
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
                "q_open": 0.89,
                "q_yesno": 0.1
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
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "残念、はずれだよ。また考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "約束を書いた紙を誰かに破られてしまい、二人は悲しくてそのまま諦めたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.75291661900701,
      "judge_s": 0.75291661900701,
      "luna_s": null,
      "total_s": 0.7529191770008765,
      "writer_s": 2.5579938665032387e-06
    }
  },
  {
    "case_id": "U18-b22",
    "record": {
      "comment_id": "U18-b22",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4091,
            "latency_s": 1.171089,
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
              "C": 0.43,
              "D": {
                "irrelevant": 0.95,
                "no": 0.04,
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
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "関係ないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "2人は直接会う約束をしてたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.171331140998518,
      "judge_s": 1.171331140998518,
      "luna_s": null,
      "total_s": 1.1713343689916655,
      "writer_s": 3.2279931474477053e-06
    }
  },
  {
    "case_id": "U18-b23",
    "record": {
      "comment_id": "U18-b23",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4115,
            "latency_s": 1.075471,
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
                "guess": 0.04,
                "question": 0.96
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.04,
                "q_yesno": 0.96
              },
              "A_bare": 0.05,
              "B": {
                "point_0": 0.05,
                "point_1": 0.01
              },
              "C": 0.46,
              "D": {
                "irrelevant": 0.0,
                "no": 0.14,
                "yes": 0.86
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい！ひとつずつ確かめていこうね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "「白紙」は紙が真っ白になったって意味？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.0757536799937952,
      "judge_s": 1.0757536799937952,
      "luna_s": null,
      "total_s": 1.0757567519904114,
      "writer_s": 3.0719966161996126e-06
    }
  },
  {
    "case_id": "U18-b24",
    "record": {
      "comment_id": "U18-b24",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4103,
            "latency_s": 1.080583,
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
                "guess": 0.52,
                "question": 0.48
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
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "はい！ひとつずつ確かめていこうね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "夏の日に何か予定外のことが起きた？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.0809014659898821,
      "judge_s": 1.0809014659898821,
      "luna_s": null,
      "total_s": 1.0809040759922937,
      "writer_s": 2.610002411529422e-06
    }
  },
  {
    "case_id": "U18-b25",
    "record": {
      "comment_id": "U18-b25",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4061,
            "latency_s": 1.174709,
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
                "guess": 0.03,
                "question": 0.97
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
        "luna": null
      },
      "media_id": "local-U18",
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
      "text": "2人は恋人同士なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.175040803005686,
      "judge_s": 1.175040803005686,
      "luna_s": null,
      "total_s": 1.1750436430156697,
      "writer_s": 2.8400099836289883e-06
    }
  },
  {
    "case_id": "U18-b26",
    "record": {
      "comment_id": "U18-b26",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4085,
            "latency_s": 1.118764,
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
                "guess": 0.78,
                "question": 0.22
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
              "C": 0.48,
              "D": {
                "irrelevant": 0.02,
                "no": 0.65,
                "yes": 0.33
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": null
      },
      "media_id": "local-U18",
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
      "text": "約束は延期になっただけなの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.119117599009769,
      "judge_s": 1.119117599009769,
      "luna_s": null,
      "total_s": 1.1191204540082254,
      "writer_s": 2.854998456314206e-06
    }
  },
  {
    "case_id": "U18-b27",
    "record": {
      "comment_id": "U18-b27",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4085,
            "latency_s": 1.439624,
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
              "C": 0.52,
              "D": {
                "irrelevant": 0.07,
                "no": 0.81,
                "yes": 0.12
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": null
      },
      "media_id": "local-U18",
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
      "text": "約束の内容は夏に関係あるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.4399994669947773,
      "judge_s": 1.4399994669947773,
      "luna_s": null,
      "total_s": 1.4400020559842233,
      "writer_s": 2.58898944593966e-06
    }
  },
  {
    "case_id": "U18-b28",
    "record": {
      "comment_id": "U18-b28",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 4055,
            "latency_s": 1.193313,
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
                "guess": 0.67,
                "question": 0.33
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
              "C": 0.37,
              "D": {
                "irrelevant": 0.93,
                "no": 0.07,
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
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "関係ないよ。なるほど、メモしておくね🧐"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "2人は子どもなの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1936466270126402,
      "judge_s": 1.1936466270126402,
      "luna_s": null,
      "total_s": 1.1936494570109062,
      "writer_s": 2.829998265951872e-06
    }
  },
  {
    "case_id": "U18-t01",
    "record": {
      "comment_id": "U18-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "消せるボールペン",
          "debug": {
            "calls": 1,
            "input_tokens": 933,
            "latency_s": 0.185786,
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
              "A_bare": 0.83
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.83"
        },
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "何が消せるボールペンなのか教えてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "消せるボールペン？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.18587024699081667,
      "judge_s": 0.18587024699081667,
      "luna_s": null,
      "total_s": 0.1858743179764133,
      "writer_s": 4.070985596626997e-06
    }
  },
  {
    "case_id": "U18-t02",
    "record": {
      "comment_id": "U18-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
      "final": {
        "answer": null,
        "decision": "jev",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "バスケットボール",
          "debug": {
            "calls": 1,
            "input_tokens": 932,
            "latency_s": 0.209964,
            "model": "jev-latest",
            "output_tokens": 78,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.09,
                "question_or_guess": 0.91,
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
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "バスケットボールが何のことか、もう少し詳しく教えて！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "バスケットボール",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.21002959899487905,
      "judge_s": 0.21002959899487905,
      "luna_s": null,
      "total_s": 0.21003287198254839,
      "writer_s": 3.2729876693338156e-06
    }
  },
  {
    "case_id": "c-ask_spoiler-01",
    "record": {
      "comment_id": "c-ask_spoiler-01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 1421,
            "latency_s": 0.371467,
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
              "A_bare": 0.1
            }
          },
          "error": null,
          "kind": "ask_spoiler",
          "reason": "段A=request→ask_spoiler"
        },
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "真相はナイショ🤭 質問で探ってごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "答えだけ教えて〜",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.37163605698151514,
      "judge_s": 0.37163605698151514,
      "luna_s": null,
      "total_s": 0.371639263961697,
      "writer_s": 3.2069801818579435e-06
    }
  },
  {
    "case_id": "c-impression-05",
    "record": {
      "comment_id": "c-impression-05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 1584,
            "latency_s": 0.376836,
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
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "ありがとう！楽しんでくれてうれしいよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "短いのに奥が深い！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.3770032500033267,
      "judge_s": 0.3770032500033267,
      "luna_s": null,
      "total_s": 0.377006191003602,
      "writer_s": 2.9410002753138542e-06
    }
  },
  {
    "case_id": "c-chat-04",
    "record": {
      "comment_id": "c-chat-04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 1592,
            "latency_s": 0.428392,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 148,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.02,
                "reaction": 0.98,
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
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "へえ、そうなんだ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "週末ってあっという間だなー",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.42856884200591594,
      "judge_s": 0.42856884200591594,
      "luna_s": null,
      "total_s": 0.42857119400287047,
      "writer_s": 2.3519969545304775e-06
    }
  },
  {
    "case_id": "c-mention-03",
    "record": {
      "comment_id": "c-mention-03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "input_tokens": 1590,
            "latency_s": 0.455056,
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
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "みんなで考えてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "@yuki こういうの好きそう",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.45518738601822406,
      "judge_s": 0.45518738601822406,
      "luna_s": null,
      "total_s": 0.45518987203831784,
      "writer_s": 2.4860200937837362e-06
    }
  },
  {
    "case_id": "c-complaint-07",
    "record": {
      "comment_id": "c-complaint-07",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
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
            "latency_s": 0.356623,
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
              "A_bare": 0.12
            }
          },
          "error": null,
          "kind": "complaint",
          "reason": "段A=reaction→complaint"
        },
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "教えてくれてありがとう。確認するね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "バカみたいな問題だな",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.35682195899426006,
      "judge_s": 0.35682195899426006,
      "luna_s": null,
      "total_s": 0.35682519199326634,
      "writer_s": 3.2329990062862635e-06
    }
  },
  {
    "case_id": "c-foreign-01",
    "record": {
      "comment_id": "c-foreign-01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "jev",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "2b",
        "shadow": false
      },
      "content_key": "007-blank-letter",
      "errors": [],
      "fact_sheet_hash": "8832e6127fa7",
      "final": {
        "answer": null,
        "decision": "jev",
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
        "luna": null
      },
      "media_id": "local-U18",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "日本語のコメントで質問してね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "That was fun!",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 6.184098310768604e-05,
      "judge_s": 6.184098310768604e-05,
      "luna_s": null,
      "total_s": 6.504496559500694e-05,
      "writer_s": 3.2039824873209e-06
    }
  }
];
