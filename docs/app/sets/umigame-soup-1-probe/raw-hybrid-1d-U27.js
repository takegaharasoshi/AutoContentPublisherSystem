window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["hybrid-1d/U27"] = [
  {
    "case_id": "U27-e01",
    "record": {
      "comment_id": "U27-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 4657,
            "latency_s": 1.236095,
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
                  "close": 0.08,
                  "hit": 0.05
                }
              },
              "C": 0.7,
              "D": {
                "irrelevant": 0.0,
                "no": 1.0,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.05"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 153,
            "finish_reason": "stop",
            "latency_s": 2.615102,
            "model": "gpt-6-luna",
            "prompt_tokens": 3253,
            "reasoning_tokens": 98
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "車は本物ではなく、家の中で動かしています。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は本物の車を公道で運転しているんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.23642866499722,
      "judge_s": 2.6151491260388866,
      "luna_s": 2.6151491260388866,
      "total_s": 3.989681481034495,
      "writer_s": 1.3745323549956083
    }
  },
  {
    "case_id": "U27-e02",
    "record": {
      "comment_id": "U27-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 4663,
            "latency_s": 1.137708,
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
                "q_multi": 0.01,
                "q_open": 0.01,
                "q_yesno": 0.98
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.11,
                  "hit": 0.09
                }
              },
              "C": 0.63,
              "D": {
                "irrelevant": 0.01,
                "no": 0.93,
                "yes": 0.06
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.09"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 357,
            "finish_reason": "stop",
            "latency_s": 4.37789,
            "model": "gpt-6-luna",
            "prompt_tokens": 3255,
            "reasoning_tokens": 283
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "運転席にいるかを尋ねる、はい・いいえで答えられる質問です。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。誰かが運転席にいる？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "妻や子どもたちの誰かが運転席にいるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.1381605720380321,
      "judge_s": 4.377945045009255,
      "luna_s": 4.377945045009255,
      "total_s": 6.954427174059674,
      "writer_s": 2.5764821290504187
    }
  },
  {
    "case_id": "U27-e03",
    "record": {
      "comment_id": "U27-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 4603,
            "latency_s": 1.207086,
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
                "guess": 0.91,
                "question": 0.09
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.03,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.58,
              "D": {
                "irrelevant": 0.0,
                "no": 1.0,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 247,
            "finish_reason": "stop",
            "latency_s": 3.331469,
            "model": "gpt-6-luna",
            "prompt_tokens": 3246,
            "reasoning_tokens": 176
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実では、車は自動運転ではなく男自身が動かしています。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "車は自動運転の車ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.2074239120120183,
      "judge_s": 3.3314979270799085,
      "luna_s": 3.3314979270799085,
      "total_s": 5.015937038115226,
      "writer_s": 1.6844391110353172
    }
  },
  {
    "case_id": "U27-e04",
    "record": {
      "comment_id": "U27-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 4711,
            "latency_s": 1.245697,
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
                "guess": 0.3,
                "question": 0.7
              },
              "A2": {
                "q_multi": 0.03,
                "q_open": 0.01,
                "q_yesno": 0.96
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.01,
                  "hit": 0.01
                }
              },
              "C": 0.67,
              "D": {
                "irrelevant": 0.02,
                "no": 0.93,
                "yes": 0.05
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
            "completion_tokens": 640,
            "finish_reason": "stop",
            "latency_s": 6.749495,
            "model": "gpt-6-luna",
            "prompt_tokens": 3259,
            "reasoning_tokens": 560
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "本物の車を運転しておらず、運転経験とは言えないため。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は運転免許を持っていないだけで、運転の経験はあるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.2459805130492896,
      "judge_s": 6.749515939038247,
      "luna_s": 6.749515939038247,
      "total_s": 8.6295925329905,
      "writer_s": 1.8800765939522535
    }
  },
  {
    "case_id": "U27-e05",
    "record": {
      "comment_id": "U27-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 4675,
            "latency_s": 1.205469,
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
                "guess": 0.65,
                "question": 0.35
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.03,
                "q_yesno": 0.97
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.01,
                  "hit": 0.01
                }
              },
              "C": 0.55,
              "D": {
                "irrelevant": 0.08,
                "no": 0.45,
                "yes": 0.47000000000000003
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
            "completion_tokens": 591,
            "finish_reason": "stop",
            "latency_s": 6.638507,
            "model": "gpt-6-luna",
            "prompt_tokens": 3255,
            "reasoning_tokens": 512
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "家族が楽しんでいることは事実ですが、移動そのものを楽しむかは示されていません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ふむふむ、ほかも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "家族は車の中で移動そのものを楽しんでるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.2057779500028118,
      "judge_s": 6.638561504078098,
      "luna_s": 6.638561504078098,
      "total_s": 8.5816510040313,
      "writer_s": 1.943089499953203
    }
  },
  {
    "case_id": "U27-e06",
    "record": {
      "comment_id": "U27-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 4669,
            "latency_s": 1.226486,
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
                "guess": 0.65,
                "question": 0.35
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
              "C": 0.67,
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
            "completion_tokens": 280,
            "finish_reason": "stop",
            "latency_s": 3.794618,
            "model": "gpt-6-luna",
            "prompt_tokens": 3253,
            "reasoning_tokens": 203
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実では、車が走るのは家の中で、遊園地などの施設ではありません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ほかのことも聞いてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "この車は遊園地などの施設の中を走るものですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.226770207984373,
      "judge_s": 3.7946420470252633,
      "luna_s": 3.7946420470252633,
      "total_s": 5.476605064002797,
      "writer_s": 1.6819630169775337
    }
  },
  {
    "case_id": "U27-e07",
    "record": {
      "comment_id": "U27-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 4645,
            "latency_s": 1.146476,
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
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.05,
                  "hit": 0.02
                }
              },
              "C": 0.7,
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
            "completion_tokens": 167,
            "finish_reason": "stop",
            "latency_s": 2.758701,
            "model": "gpt-6-luna",
            "prompt_tokens": 3251,
            "reasoning_tokens": 99
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、男は車の外から自分で動かしているとあります。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！車の外から車を動かしてるんだね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は車の外から車を動かしてるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.1467082030139863,
      "judge_s": 2.7587675499962643,
      "luna_s": 2.7587675499962643,
      "total_s": 4.769986249972135,
      "writer_s": 2.0112186999758705
    }
  },
  {
    "case_id": "U27-e08",
    "record": {
      "comment_id": "U27-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
      "final": {
        "answer": "no",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4675,
            "latency_s": 1.242688,
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
                  "close": 0.03,
                  "hit": 0.02
                }
              },
              "C": 0.65,
              "D": {
                "irrelevant": 0.52,
                "no": 0.38,
                "yes": 0.1
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
            "completion_tokens": 1487,
            "finish_reason": "stop",
            "latency_s": 14.05011,
            "model": "gpt-6-luna",
            "prompt_tokens": 3256,
            "reasoning_tokens": 1397
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "実際の家族は長距離を移動せず、集まって遊んでいます。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "家族は長い距離を何時間もかけて移動するんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.243015912012197,
      "judge_s": 14.050188582972623,
      "luna_s": 14.050188582972623,
      "total_s": 15.484739750972949,
      "writer_s": 1.4345511680003256
    }
  },
  {
    "case_id": "U27-e09",
    "record": {
      "comment_id": "U27-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 4645,
            "latency_s": 1.306354,
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
                  "close": 0.04,
                  "hit": 0.03
                }
              },
              "C": 0.41,
              "D": {
                "irrelevant": 0.01,
                "no": 0.99,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.03"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 365,
            "finish_reason": "stop",
            "latency_s": 4.450139,
            "model": "gpt-6-luna",
            "prompt_tokens": 3250,
            "reasoning_tokens": 293
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "走っているのは実車ではなく、ガソリンで走る車ではありません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ガソリンで走る車ではないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "乗っているのはガソリンで走る車ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.3067298750393093,
      "judge_s": 4.450222149956971,
      "luna_s": 4.450222149956971,
      "total_s": 7.272994071943685,
      "writer_s": 2.822771921986714
    }
  },
  {
    "case_id": "U27-e10",
    "record": {
      "comment_id": "U27-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 4651,
            "latency_s": 1.20843,
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
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.05,
                  "hit": 0.03
                }
              },
              "C": 0.77,
              "D": {
                "irrelevant": 0.0,
                "no": 0.97,
                "yes": 0.03
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.03"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 192,
            "finish_reason": "stop",
            "latency_s": 3.517909,
            "model": "gpt-6-luna",
            "prompt_tokens": 3251,
            "reasoning_tokens": 132
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "車内でハンドルを握る運転はしていないと確定しています。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。自分でハンドルを操作してはいないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は自分でハンドルを操作してるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.2087204629788175,
      "judge_s": 3.5179673889651895,
      "luna_s": 3.5179673889651895,
      "total_s": 5.622501743026078,
      "writer_s": 2.1045343540608883
    }
  },
  {
    "case_id": "U27-e11",
    "record": {
      "comment_id": "U27-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 2150,
            "latency_s": 0.586324,
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
                "guess": 0.36,
                "question": 0.64
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
            "completion_tokens": 154,
            "finish_reason": "stop",
            "latency_s": 2.225655,
            "model": "gpt-6-luna",
            "prompt_tokens": 3260,
            "reasoning_tokens": 83
          },
          "error": null,
          "kind": "q_multi",
          "reason": "はい・いいえで答えられる質問が二つあります。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつしてね。まずはどちらか聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "車は実際に道路を走ってるの？男以外の誰かが運転してるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.5865205650916323,
      "judge_s": 2.225691743893549,
      "luna_s": 2.225691743893549,
      "total_s": 3.741203364916146,
      "writer_s": 1.515511621022597
    }
  },
  {
    "case_id": "U27-e12",
    "record": {
      "comment_id": "U27-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "latency_s": 0.591884,
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
                "guess": 0.9,
                "question": 0.1
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
            "completion_tokens": 172,
            "finish_reason": "stop",
            "latency_s": 2.504624,
            "model": "gpt-6-luna",
            "prompt_tokens": 3258,
            "reasoning_tokens": 88
          },
          "error": null,
          "kind": "q_multi",
          "reason": "遊園地の乗り物か、家族が運転ごっこをしているかの二つを尋ねています。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。どっちから聞いてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "これは遊園地の乗り物なの？家族は運転ごっこをしてるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.5920637579401955,
      "judge_s": 2.5046817070106044,
      "luna_s": 2.5046817070106044,
      "total_s": 4.362174037029035,
      "writer_s": 1.857492330018431
    }
  },
  {
    "case_id": "U27-e13",
    "record": {
      "comment_id": "U27-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 2676,
            "latency_s": 0.797509,
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
            "completion_tokens": 175,
            "finish_reason": "stop",
            "latency_s": 2.773938,
            "model": "gpt-6-luna",
            "prompt_tokens": 3256,
            "reasoning_tokens": 98
          },
          "error": null,
          "kind": "q_open",
          "reason": "「どうやって」と方法を尋ねる、はい／いいえで答えられない質問です。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "「男は自分で運転しているの？」のように、はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "免許がない男は、どうやって車を走らせているんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.7977912040660158,
      "judge_s": 2.7739575289888307,
      "luna_s": 2.7739575289888307,
      "total_s": 6.032721093972214,
      "writer_s": 3.258763564983383
    }
  },
  {
    "case_id": "U27-e14",
    "record": {
      "comment_id": "U27-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "latency_s": 0.745952,
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
                "guess": 0.08,
                "question": 0.92
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.97,
                "q_yesno": 0.02
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
            "completion_tokens": 309,
            "finish_reason": "stop",
            "latency_s": 3.527445,
            "model": "gpt-6-luna",
            "prompt_tokens": 3254,
            "reasoning_tokens": 224
          },
          "error": null,
          "kind": "q_open",
          "reason": "「誰の運転か」を尋ねる、はい／いいえで答えられない質問です。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "運転しているのは男なのかな？はい・いいえで答えられる形で聞いてみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "妻と子どもたちは誰の運転で移動しているんでしょう？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.7462099329568446,
      "judge_s": 3.5275092771044,
      "luna_s": 3.5275092771044,
      "total_s": 6.255754587124102,
      "writer_s": 2.7282453100197017
    }
  },
  {
    "case_id": "U27-e15",
    "record": {
      "comment_id": "U27-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "latency_s": 0.828863,
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
                "guess": 0.0,
                "question": 1.0
              },
              "A2": {
                "q_multi": 0.04,
                "q_open": 0.96,
                "q_yesno": 0.0
              },
              "A3": 0.04,
              "A_bare": 0.05
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
            "completion_tokens": 210,
            "finish_reason": "stop",
            "latency_s": 2.581518,
            "model": "gpt-6-luna",
            "prompt_tokens": 3255,
            "reasoning_tokens": 116
          },
          "error": null,
          "kind": "q_open",
          "reason": "「どこからどこまで」と場所を尋ねる、はい・いいえで答えられない質問です。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる質問にして聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "「長い道のり」とは、どこからどこまでのことですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.8292365130037069,
      "judge_s": 2.5815622550435364,
      "luna_s": 2.5815622550435364,
      "total_s": 5.507399016059935,
      "writer_s": 2.9258367610163987
    }
  },
  {
    "case_id": "U27-e16",
    "record": {
      "comment_id": "U27-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 2390,
            "latency_s": 0.618896,
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
              "A_bare": 0.06,
              "B": {
                "point_0": {
                  "close": 0.9199999999999999,
                  "hit": 0.45
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.45"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 410,
            "finish_reason": "stop",
            "latency_s": 4.362091,
            "model": "gpt-6-luna",
            "prompt_tokens": 3250,
            "reasoning_tokens": 345
          },
          "error": null,
          "kind": "guess_close",
          "reason": "人生ゲームの車の駒には触れていますが、家族がピンだとは述べていません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！ほかの可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "人生ゲームの車の駒を動かしてたってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.6191131770610809,
      "judge_s": 4.362159913987853,
      "luna_s": 4.362159913987853,
      "total_s": 6.469622972887009,
      "writer_s": 2.1074630588991567
    }
  },
  {
    "case_id": "U27-e17",
    "record": {
      "comment_id": "U27-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 2477,
            "latency_s": 0.637347,
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
                  "close": 0.96,
                  "hit": 0.31
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.31"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 174,
            "finish_reason": "stop",
            "latency_s": 2.884468,
            "model": "gpt-6-luna",
            "prompt_tokens": 3276,
            "reasoning_tokens": 108
          },
          "error": null,
          "kind": "guess_close",
          "reason": "人生ゲームの車の駒は当てていますが、家族がピンである点には触れていません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！ほかの可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "家族で人生ゲームをしていて、男が車の駒を盤の道に沿って進めてたんだね。免許がなくてもできるわけだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.637566905003041,
      "judge_s": 2.884519605897367,
      "luna_s": 2.884519605897367,
      "total_s": 4.392401495948434,
      "writer_s": 1.5078818900510669
    }
  },
  {
    "case_id": "U27-e18",
    "record": {
      "comment_id": "U27-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 2435,
            "latency_s": 0.615642,
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
                  "hit": 0.09
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.09"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 186,
            "finish_reason": "stop",
            "latency_s": 2.810077,
            "model": "gpt-6-luna",
            "prompt_tokens": 3268,
            "reasoning_tokens": 122
          },
          "error": null,
          "kind": "guess_close",
          "reason": "すごろくの車の駒には触れていますが、核心の特定には至っていません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し考えてみようか😉"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "家族で何かのすごろくをしていて、車の駒を長い道に沿って進めてるんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.6159098299685866,
      "judge_s": 2.810096140950918,
      "luna_s": 2.810096140950918,
      "total_s": 4.210139285889454,
      "writer_s": 1.400043144938536
    }
  },
  {
    "case_id": "U27-e19",
    "record": {
      "comment_id": "U27-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 2477,
            "latency_s": 0.634127,
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
                  "close": 0.87,
                  "hit": 0.16
                }
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
            "completion_tokens": 175,
            "finish_reason": "stop",
            "latency_s": 2.815561,
            "model": "gpt-6-luna",
            "prompt_tokens": 3278,
            "reasoning_tokens": 115
          },
          "error": null,
          "kind": "guess_close",
          "reason": "車の正体には触れていますが、家族が嫌々という誤りがあります。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し考えてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "人生ゲームの車の駒を進めてるんだね。楽しんでるのは男だけで、妻と子どもは嫌々付き合わされてるのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.634497398044914,
      "judge_s": 2.815609961980954,
      "luna_s": 2.815609961980954,
      "total_s": 4.680726932943799,
      "writer_s": 1.8651169709628448
    }
  },
  {
    "case_id": "U27-e20",
    "record": {
      "comment_id": "U27-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 4717,
            "latency_s": 1.26137,
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
                "q_multi": 0.01,
                "q_open": 0.05,
                "q_yesno": 0.94
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.33,
              "D": {
                "irrelevant": 0.0,
                "no": 1.0,
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
            "completion_tokens": 226,
            "finish_reason": "stop",
            "latency_s": 2.876589,
            "model": "gpt-6-luna",
            "prompt_tokens": 3259,
            "reasoning_tokens": 148
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "妻が運転するという推理で、人生ゲームの駒という核心には触れていません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "妻が運転していて、男は助手席から道案内をしてるだけなんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.261751738958992,
      "judge_s": 2.876650599995628,
      "luna_s": 2.876650599995628,
      "total_s": 4.184189424035139,
      "writer_s": 1.3075388240395114
    }
  },
  {
    "case_id": "U27-e21",
    "record": {
      "comment_id": "U27-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 2975,
            "latency_s": 0.838524,
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
                "q_open": 0.64,
                "q_yesno": 0.32
              },
              "A_bare": 0.03,
              "B": {
                "point_0": {
                  "close": 0.01,
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
            "completion_tokens": 273,
            "finish_reason": "stop",
            "latency_s": 3.572679,
            "model": "gpt-6-luna",
            "prompt_tokens": 3266,
            "reasoning_tokens": 193
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "遊園地の乗り物は核心のボードゲームの駒に触れていません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "車型の遊園地の乗り物に家族で乗って、男が運転手役をしてるんだと思う。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.8387906800489873,
      "judge_s": 3.5727398929884657,
      "luna_s": 3.5727398929884657,
      "total_s": 4.87241345399525,
      "writer_s": 1.2996735610067844
    }
  },
  {
    "case_id": "U27-k01",
    "record": {
      "comment_id": "U27-k01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 3744,
            "latency_s": 0.823398,
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
                  "close": 0.88,
                  "hit": 0.67
                }
              },
              "B2": 0.06
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.67, 矛盾=0.06"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 299,
            "finish_reason": "stop",
            "latency_s": 3.518046,
            "model": "gpt-6-luna",
            "prompt_tokens": 3267,
            "reasoning_tokens": 195
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "人生ゲームの車の駒と、家族を表すピンの両方を当てています。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！男が走らせているのは人生ゲームの車の駒。妻と子どもはピンで乗せていて、おもちゃなので免許はいらない。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "車も家族も盤上のコマやピンで、男は人生ゲームの長い道を進めていたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.8236677899258211,
      "judge_s": 3.518070026068017,
      "luna_s": 3.518070026068017,
      "total_s": 3.5180876831291243,
      "writer_s": 1.7657061107456684e-05
    }
  },
  {
    "case_id": "U27-k02",
    "record": {
      "comment_id": "U27-k02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 3748,
            "latency_s": 0.844923,
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
              "A_bare": 0.03,
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
            "completion_tokens": 207,
            "finish_reason": "stop",
            "latency_s": 2.647374,
            "model": "gpt-6-luna",
            "prompt_tokens": 3265,
            "reasoning_tokens": 105
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "人生ゲームの車の駒と、家族を表すピンの両方を当てています。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！男が走らせているのは人生ゲームの車の駒。妻と子どもはピンで乗せていて、おもちゃなので免許はいらない。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "ゲームの車コマに家族を表すピンを挿して、人生ゲームで道を進んでいたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.8451832579448819,
      "judge_s": 2.6474485140061006,
      "luna_s": 2.6474485140061006,
      "total_s": 2.6474551639985293,
      "writer_s": 6.649992428719997e-06
    }
  },
  {
    "case_id": "U27-k03",
    "record": {
      "comment_id": "U27-k03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 2435,
            "latency_s": 0.551466,
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
                  "close": 0.92,
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
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 295,
            "finish_reason": "stop",
            "latency_s": 3.608734,
            "model": "gpt-6-luna",
            "prompt_tokens": 3264,
            "reasoning_tokens": 234
          },
          "error": null,
          "kind": "guess_close",
          "reason": "ボードゲームの要素には触れていますが、核心の特定には至っていません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し推理を続けてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "家族でボードゲームを囲み、車のおもちゃを盤の道に沿って進めていたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.5517273619771004,
      "judge_s": 3.6087601630715653,
      "luna_s": 3.6087601630715653,
      "total_s": 4.981513827107847,
      "writer_s": 1.3727536640362814
    }
  },
  {
    "case_id": "U27-k04",
    "record": {
      "comment_id": "U27-k04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 2453,
            "latency_s": 0.608157,
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
                "point_0": {
                  "close": 0.93,
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
            "completion_tokens": 241,
            "finish_reason": "stop",
            "latency_s": 3.280289,
            "model": "gpt-6-luna",
            "prompt_tokens": 3270,
            "reasoning_tokens": 173
          },
          "error": null,
          "kind": "guess_close",
          "reason": "すごろくの車の駒には触れていますが、家族が付き合っているだけという誤りがあります。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！推理を続けてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "すごろくの車コマを進めてたんだね。でも家族は一緒に楽しまず、男につき合ってるだけか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.6083962159464136,
      "judge_s": 3.2803119150921702,
      "luna_s": 3.2803119150921702,
      "total_s": 4.695458855014294,
      "writer_s": 1.4151469399221241
    }
  },
  {
    "case_id": "U27-k05",
    "record": {
      "comment_id": "U27-k05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 2390,
            "latency_s": 0.619045,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 150,
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
              "A_bare": 0.05,
              "B": {
                "point_0": {
                  "close": 0.99,
                  "hit": 0.07
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.07"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 245,
            "finish_reason": "stop",
            "latency_s": 3.004775,
            "model": "gpt-6-luna",
            "prompt_tokens": 3254,
            "reasoning_tokens": 172
          },
          "error": null,
          "kind": "guess_close",
          "reason": "盤上で動かす遊びのコマには触れていますが、人生ゲームや家族のピンまでは特定できていません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！ほかの可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "車は盤の上で動かす遊びのコマだったんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.619183189002797,
      "judge_s": 3.0048159090802073,
      "luna_s": 3.0048159090802073,
      "total_s": 5.12817038805224,
      "writer_s": 2.1233544789720327
    }
  },
  {
    "case_id": "U27-k06",
    "record": {
      "comment_id": "U27-k06",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 2959,
            "latency_s": 0.848239,
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
                "q_multi": 0.03,
                "q_open": 0.74,
                "q_yesno": 0.23
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.04,
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
            "completion_tokens": 210,
            "finish_reason": "stop",
            "latency_s": 3.079815,
            "model": "gpt-6-luna",
            "prompt_tokens": 3262,
            "reasoning_tokens": 146
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "妻が本物の車を運転するという推理で、核心には触れていません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "妻が本物の車を運転し、男は助手席から家族に道を教えてたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.8483896739780903,
      "judge_s": 3.0798757049487904,
      "luna_s": 3.0798757049487904,
      "total_s": 4.412496076896787,
      "writer_s": 1.3326203719479963
    }
  },
  {
    "case_id": "U27-t01",
    "record": {
      "comment_id": "U27-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "3fa8694b418f",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "人生ゲーム",
          "debug": {
            "calls": 1,
            "input_tokens": 930,
            "latency_s": 0.1738,
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
              "A_bare": 0.87
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.87"
        },
        "luna": {
          "answer": null,
          "bare_term": "人生ゲーム",
          "debug": {
            "completion_tokens": 215,
            "finish_reason": "stop",
            "latency_s": 2.628041,
            "model": "gpt-6-luna",
            "prompt_tokens": 3238,
            "reasoning_tokens": 138
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句だけのコメントなので、はい・いいえで答えられません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "人生ゲームが何のことか、もう少し詳しく教えて！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "人生ゲーム？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.17389801901299506,
      "judge_s": 2.62809821695555,
      "luna_s": 2.62809821695555,
      "total_s": 4.243890055920929,
      "writer_s": 1.6157918389653787
    }
  },
  {
    "case_id": "U27-t02",
    "record": {
      "comment_id": "U27-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "3fa8694b418f",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "遊園地",
          "debug": {
            "calls": 1,
            "input_tokens": 927,
            "latency_s": 0.198422,
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
          "bare_term": "遊園地",
          "debug": {
            "completion_tokens": 190,
            "finish_reason": "stop",
            "latency_s": 2.444646,
            "model": "gpt-6-luna",
            "prompt_tokens": 3238,
            "reasoning_tokens": 105
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句のみのコメントなので、質問として聞き直しを促します。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "遊園地が何のことか、もう少し詳しく教えて！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "遊園地",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.1985006429022178,
      "judge_s": 2.444705122965388,
      "luna_s": 2.444705122965388,
      "total_s": 5.5400015959749,
      "writer_s": 3.095296473009512
    }
  },
  {
    "case_id": "c-ask_howto-03",
    "record": {
      "comment_id": "c-ask_howto-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 1435,
            "latency_s": 0.404796,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 124,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.25,
                "reaction": 0.04,
                "request": 0.71
              },
              "A2": {
                "ask_hint": 0.01,
                "ask_howto": 0.98,
                "ask_spoiler": 0.01
              },
              "A_bare": 0.06
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
            "completion_tokens": 217,
            "finish_reason": "stop",
            "latency_s": 2.73827,
            "model": "gpt-6-luna",
            "prompt_tokens": 3246,
            "reasoning_tokens": 143
          },
          "error": null,
          "kind": "ask_howto",
          "reason": "遊び方として、回答形式を確認している質問です。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "うん！はい・いいえで答えられる質問をコメントしてごらん。私が答えるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "はい・いいえで答えればいい感じ？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.40496305807027966,
      "judge_s": 2.7383253909647465,
      "luna_s": 2.7383253909647465,
      "total_s": 4.472839824971743,
      "writer_s": 1.7345144340069965
    }
  },
  {
    "case_id": "c-cheer-02",
    "record": {
      "comment_id": "c-cheer-02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 1580,
            "latency_s": 0.392137,
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
              "A_bare": 0.07
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
            "completion_tokens": 146,
            "finish_reason": "stop",
            "latency_s": 2.475487,
            "model": "gpt-6-luna",
            "prompt_tokens": 3240,
            "reasoning_tokens": 87
          },
          "error": null,
          "kind": "cheer",
          "reason": "応援の言葉なので、励ましに対するお礼を返します。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ありがとう！楽しく推理していこうね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "応援してます！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.392305968911387,
      "judge_s": 2.4755318589741364,
      "luna_s": 2.4755318589741364,
      "total_s": 4.225885457010008,
      "writer_s": 1.750353598035872
    }
  },
  {
    "case_id": "c-complaint-01",
    "record": {
      "comment_id": "c-complaint-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "latency_s": 0.48543,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 149,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.04,
                "reaction": 0.7,
                "request": 0.26
              },
              "A2": {
                "chat": 0.0,
                "cheer": 0.0,
                "complaint": 0.97,
                "greeting": 0.0,
                "impression": 0.01,
                "mention": 0.0,
                "request": 0.02
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
            "completion_tokens": 133,
            "finish_reason": "stop",
            "latency_s": 2.187007,
            "model": "gpt-6-luna",
            "prompt_tokens": 3245,
            "reasoning_tokens": 74
          },
          "error": null,
          "kind": "complaint",
          "reason": "問題の説明が足りないという、問題への指摘です。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "教えてくれてありがとう。確認するね！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "これちょっと説明足りなくない？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.48558776907157153,
      "judge_s": 2.1870311700040475,
      "luna_s": 2.1870311700040475,
      "total_s": 3.781137289945036,
      "writer_s": 1.5941061199409887
    }
  },
  {
    "case_id": "c-emoji_only-05",
    "record": {
      "comment_id": "c-emoji_only-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "completion_tokens": 98,
            "finish_reason": "stop",
            "latency_s": 1.939922,
            "model": "gpt-6-luna",
            "prompt_tokens": 3244,
            "reasoning_tokens": 50
          },
          "error": null,
          "kind": "emoji_only",
          "reason": "絵文字のみのコメントです。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "コメントありがとう☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "🕵️‍♂️❓",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 7.738207932561636e-05,
      "judge_s": 1.9399736550403759,
      "luna_s": 1.9399736550403759,
      "total_s": 3.514852807042189,
      "writer_s": 1.574879152001813
    }
  },
  {
    "case_id": "c-spam-04",
    "record": {
      "comment_id": "c-spam-04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 1478,
            "latency_s": 0.400833,
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
              "A_bare": 0.11
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
            "completion_tokens": 87,
            "finish_reason": "stop",
            "latency_s": 1.859568,
            "model": "gpt-6-luna",
            "prompt_tokens": 3243,
            "reasoning_tokens": 36
          },
          "error": null,
          "kind": "spam",
          "reason": "投資案件の紹介とDMへの誘導を含む宣伝です。"
        }
      },
      "media_id": "local-U27",
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
      "text": "投資案件紹介中！DMください",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.40104221599176526,
      "judge_s": 1.8596268029650673,
      "luna_s": 1.8596268029650673,
      "total_s": 1.8596337100025266,
      "writer_s": 6.9070374593138695e-06
    }
  },
  {
    "case_id": "c-abuse-08",
    "record": {
      "comment_id": "c-abuse-08",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 1486,
            "latency_s": 0.410395,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
            "probabilities": {
              "A1": {
                "inappropriate": 0.98,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.0,
                "request": 0.02
              },
              "A2": {
                "abuse": 0.95,
                "personal_info": 0.03,
                "spam": 0.0,
                "troll": 0.02
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
            "completion_tokens": 185,
            "finish_reason": "stop",
            "latency_s": 2.62009,
            "model": "gpt-6-luna",
            "prompt_tokens": 3250,
            "reasoning_tokens": 135
          },
          "error": null,
          "kind": "abuse",
          "reason": "作者に対する性的な画像の要求にあたるため。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "みんなが楽しめる言葉でお願いね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "作者の顔写真あげてよ、脱いでるやつ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.41058034100569785,
      "judge_s": 2.620148138026707,
      "luna_s": 2.620148138026707,
      "total_s": 2.6201590440468863,
      "writer_s": 1.0906020179390907e-05
    }
  }
];
