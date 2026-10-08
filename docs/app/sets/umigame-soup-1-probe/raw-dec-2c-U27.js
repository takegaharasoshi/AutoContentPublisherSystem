window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["dec-2c/U27"] = [
  {
    "case_id": "U27-e01",
    "record": {
      "comment_id": "U27-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "qg": 1.0
              },
              "A2": {
                "kind": 0.97
              },
              "B": {
                "point_0": 0.99
              },
              "C": {},
              "D": {
                "answer": 1.0
              }
            },
            "input_tokens": 3216,
            "latency_s": 1.411752,
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
                "q_open": 0.01,
                "q_yesno": 0.98
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.01,
                  "hit": 0.01
                }
              },
              "C": 0.67,
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
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "jev": null,
        "luna": null
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
      "shadow_mismatch": null,
      "text": "男は本物の車を公道で運転しているんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.4120680120540783,
      "jev_s": null,
      "judge_s": 1.4120680120540783,
      "luna_s": null,
      "total_s": 4.18452633311972,
      "writer_s": 2.772458321065642
    }
  },
  {
    "case_id": "U27-e02",
    "record": {
      "comment_id": "U27-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "qg": 0.96
              },
              "A2": {
                "kind": 0.97
              },
              "B": {
                "point_0": 0.97
              },
              "C": {},
              "D": {
                "answer": 0.88
              }
            },
            "input_tokens": 3228,
            "latency_s": 1.360932,
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
                  "close": 0.02,
                  "hit": 0.01
                }
              },
              "C": 0.46,
              "D": {
                "irrelevant": 0.03,
                "no": 0.92,
                "yes": 0.05
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。誰かが運転席にいるのかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "妻や子どもたちの誰かが運転席にいるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.3612047201022506,
      "jev_s": null,
      "judge_s": 1.3612047201022506,
      "luna_s": null,
      "total_s": 3.71925574215129,
      "writer_s": 2.3580510220490396
    }
  },
  {
    "case_id": "U27-e03",
    "record": {
      "comment_id": "U27-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "qg": 0.5
              },
              "A2": {
                "kind": 1.0
              },
              "B": {
                "point_0": 0.97
              },
              "C": {},
              "D": {
                "answer": 1.0
              }
            },
            "input_tokens": 3174,
            "latency_s": 1.362001,
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
                "guess": 0.25,
                "question": 0.75
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.02,
                  "hit": 0.01
                }
              },
              "C": 0.82,
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
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。その調子で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "車は自動運転の車ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.3623149079503492,
      "jev_s": null,
      "judge_s": 1.3623149079503492,
      "luna_s": null,
      "total_s": 3.4090571179986,
      "writer_s": 2.046742210048251
    }
  },
  {
    "case_id": "U27-e04",
    "record": {
      "comment_id": "U27-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "qg": 1.0
              },
              "A2": {
                "kind": 0.97
              },
              "B": {
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.69
              }
            },
            "input_tokens": 3252,
            "latency_s": 1.463763,
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
              "C": 0.38,
              "D": {
                "irrelevant": 0.03,
                "no": 0.18,
                "yes": 0.79
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
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は運転免許を持っていないだけで、運転の経験はあるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.4641333690378815,
      "jev_s": null,
      "judge_s": 1.4641333690378815,
      "luna_s": null,
      "total_s": 3.1800526031292975,
      "writer_s": 1.715919234091416
    }
  },
  {
    "case_id": "U27-e05",
    "record": {
      "comment_id": "U27-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "qg": 0.74
              },
              "A2": {
                "kind": 0.97
              },
              "B": {
                "point_0": 0.99
              },
              "C": {},
              "D": {
                "answer": 0.35
              }
            },
            "input_tokens": 3228,
            "latency_s": 1.384776,
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
                "guess": 0.13,
                "question": 0.87
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.01,
                "q_yesno": 0.98
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.01,
                  "hit": 0.0
                }
              },
              "C": 0.2,
              "D": {
                "irrelevant": 0.01,
                "no": 0.42,
                "yes": 0.57
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
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "家族は車の中で移動そのものを楽しんでるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.3850893570343032,
      "jev_s": null,
      "judge_s": 1.3850893570343032,
      "luna_s": null,
      "total_s": 3.026945114135742,
      "writer_s": 1.641855757101439
    }
  },
  {
    "case_id": "U27-e06",
    "record": {
      "comment_id": "U27-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "qg": 1.0
              },
              "A2": {
                "kind": 1.0
              },
              "B": {
                "point_0": 0.91
              },
              "C": {},
              "D": {
                "answer": 0.97
              }
            },
            "input_tokens": 3216,
            "latency_s": 1.321226,
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
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.060000000000000005,
                  "hit": 0.01
                }
              },
              "C": 0.8,
              "D": {
                "irrelevant": 0.0,
                "no": 0.98,
                "yes": 0.02
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "jev": null,
        "luna": null
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
      "shadow_mismatch": null,
      "text": "この車は遊園地などの施設の中を走るものですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.3214188510319218,
      "jev_s": null,
      "judge_s": 1.3214188510319218,
      "luna_s": null,
      "total_s": 3.416316027054563,
      "writer_s": 2.0948971760226414
    }
  },
  {
    "case_id": "U27-e07",
    "record": {
      "comment_id": "U27-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "qg": 0.96
              },
              "A2": {
                "kind": 0.97
              },
              "B": {
                "point_0": 0.97
              },
              "C": {},
              "D": {
                "answer": 0.99
              }
            },
            "input_tokens": 3204,
            "latency_s": 1.322393,
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
                  "close": 0.02,
                  "hit": 0.01
                }
              },
              "C": 0.71,
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
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！男は車の外から車を動かしてるんだね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は車の外から車を動かしてるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.3227290430804715,
      "jev_s": null,
      "judge_s": 1.3227290430804715,
      "luna_s": null,
      "total_s": 4.220489727100357,
      "writer_s": 2.897760684019886
    }
  },
  {
    "case_id": "U27-e08",
    "record": {
      "comment_id": "U27-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "kind": 0.96
              },
              "B": {
                "point_0": 1.0
              },
              "C": {}
            },
            "input_tokens": 2406,
            "latency_s": 1.149113,
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
                "q_open": 0.02,
                "q_yesno": 0.97
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.05
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
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞いてごらん。誰のことか分かるようにするといいよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "家族は長い距離を何時間もかけて移動するんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.149370622006245,
      "jev_s": null,
      "judge_s": 1.149370622006245,
      "luna_s": null,
      "total_s": 3.9659994669491425,
      "writer_s": 2.8166288449428976
    }
  },
  {
    "case_id": "U27-e09",
    "record": {
      "comment_id": "U27-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.89
              }
            },
            "input_tokens": 3198,
            "latency_s": 1.793299,
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
                }
              },
              "C": 0.28,
              "D": {
                "irrelevant": 0.03,
                "no": 0.93,
                "yes": 0.04
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
      "shadow_mismatch": null,
      "text": "乗っているのはガソリンで走る車ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.7939134949119762,
      "jev_s": null,
      "judge_s": 1.7939134949119762,
      "luna_s": null,
      "total_s": 4.6050063688308,
      "writer_s": 2.811092873918824
    }
  },
  {
    "case_id": "U27-e10",
    "record": {
      "comment_id": "U27-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "kind": 0.99
              },
              "B": {
                "point_0": 0.97
              },
              "C": {},
              "D": {
                "answer": 1.0
              }
            },
            "input_tokens": 3204,
            "latency_s": 1.447149,
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
                  "close": 0.02,
                  "hit": 0.01
                }
              },
              "C": 0.56,
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
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。自分でハンドルを操作してるんじゃないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は自分でハンドルを操作してるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.4475036050425842,
      "jev_s": null,
      "judge_s": 1.4475036050425842,
      "luna_s": null,
      "total_s": 6.201853388105519,
      "writer_s": 4.754349783062935
    }
  },
  {
    "case_id": "U27-e11",
    "record": {
      "comment_id": "U27-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "qg": 0.98
              },
              "A2": {
                "kind": 0.97
              }
            },
            "input_tokens": 1522,
            "latency_s": 1.098025,
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
                "q_multi": 0.98,
                "q_open": 0.0,
                "q_yesno": 0.02
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
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問は1つずつコメントしてね。まずはどっちから聞こうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "車は実際に道路を走ってるの？男以外の誰かが運転してるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.0982001220108941,
      "jev_s": null,
      "judge_s": 1.0982001220108941,
      "luna_s": null,
      "total_s": 3.1840702230110765,
      "writer_s": 2.0858701010001823
    }
  },
  {
    "case_id": "U27-e12",
    "record": {
      "comment_id": "U27-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "qg": 0.06
              },
              "A2": {
                "kind": 0.86
              }
            },
            "input_tokens": 1516,
            "latency_s": 0.725532,
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
                "guess": 0.53,
                "question": 0.47
              },
              "A2": {
                "q_multi": 0.91,
                "q_open": 0.0,
                "q_yesno": 0.09
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
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問は1つずつコメントしてね。どっちから聞いてみる？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "これは遊園地の乗り物なの？家族は運転ごっこをしてるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.7257629989180714,
      "jev_s": null,
      "judge_s": 0.7257629989180714,
      "luna_s": null,
      "total_s": 2.7281213778769597,
      "writer_s": 2.0023583789588884
    }
  },
  {
    "case_id": "U27-e13",
    "record": {
      "comment_id": "U27-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "major": 0.98
              },
              "A1b": {
                "qg": 0.84
              },
              "A2": {
                "kind": 0.97
              },
              "A3": {}
            },
            "input_tokens": 1883,
            "latency_s": 0.927458,
            "major": "question",
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
                "guess": 0.08,
                "question": 0.92
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.98,
                "q_yesno": 0.02
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
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形にして、聞き直してみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "免許がない男は、どうやって車を走らせているんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.9276692370185629,
      "jev_s": null,
      "judge_s": 0.9276692370185629,
      "luna_s": null,
      "total_s": 2.554008567938581,
      "writer_s": 1.6263393309200183
    }
  },
  {
    "case_id": "U27-e14",
    "record": {
      "comment_id": "U27-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "kind": 0.96
              },
              "A3": {}
            },
            "input_tokens": 1875,
            "latency_s": 0.983543,
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
                "q_open": 0.97,
                "q_yesno": 0.02
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
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "「運転しているのは〇〇？」のように、はい・いいえで答えられる形で聞いてみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "妻と子どもたちは誰の運転で移動しているんでしょう？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.983764030970633,
      "jev_s": null,
      "judge_s": 0.983764030970633,
      "luna_s": null,
      "total_s": 4.498365921899676,
      "writer_s": 3.5146018909290433
    }
  },
  {
    "case_id": "U27-e15",
    "record": {
      "comment_id": "U27-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "qg": 0.94
              },
              "A2": {
                "kind": 0.94
              },
              "A3": {}
            },
            "input_tokens": 1879,
            "latency_s": 1.011609,
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
                "q_multi": 0.0,
                "q_open": 0.96,
                "q_yesno": 0.04
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
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞き直してみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "「長い道のり」とは、どこからどこまでのことですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.0119031590875238,
      "jev_s": null,
      "judge_s": 1.0119031590875238,
      "luna_s": null,
      "total_s": 3.381048534065485,
      "writer_s": 2.369145374977961
    }
  },
  {
    "case_id": "U27-e16",
    "record": {
      "comment_id": "U27-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "point_0": 0.2
              }
            },
            "input_tokens": 1705,
            "latency_s": 0.67584,
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
                  "close": 0.6799999999999999,
                  "hit": 0.47
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
          "reason": "段A=guess→guess_close, 要点最低=0.47"
        },
        "jev": null,
        "luna": null
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
      "shadow_mismatch": null,
      "text": "人生ゲームの車の駒を動かしてたってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.6760774638969451,
      "jev_s": null,
      "judge_s": 0.6760774638969451,
      "luna_s": null,
      "total_s": 2.0993769909255207,
      "writer_s": 1.4232995270285755
    }
  },
  {
    "case_id": "U27-e17",
    "record": {
      "comment_id": "U27-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "qg": 1.0
              },
              "B": {
                "point_0": 0.49
              },
              "B2": {}
            },
            "input_tokens": 2781,
            "latency_s": 0.937854,
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
                  "close": 0.9400000000000001,
                  "hit": 0.66
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
          "reason": "段A=guess→guess_correct, 要点最低=0.66, 矛盾=0.00"
        },
        "jev": null,
        "luna": null
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
      "shadow_mismatch": null,
      "text": "家族で人生ゲームをしていて、男が車の駒を盤の道に沿って進めてたんだね。免許がなくてもできるわけだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.9382563630351797,
      "jev_s": null,
      "judge_s": 0.9382563630351797,
      "luna_s": null,
      "total_s": 0.938268783967942,
      "writer_s": 1.242093276232481e-05
    }
  },
  {
    "case_id": "U27-e18",
    "record": {
      "comment_id": "U27-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "qg": 0.96
              },
              "B": {
                "point_0": 0.79
              }
            },
            "input_tokens": 1759,
            "latency_s": 0.732273,
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
                "guess": 0.98,
                "question": 0.02
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.98,
                  "hit": 0.12
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
          "reason": "段A=guess→guess_close, 要点最低=0.12"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！ほかの可能性も考えながら、推理を続けてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "家族で何かのすごろくをしていて、車の駒を長い道に沿って進めてるんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.7325296710478142,
      "jev_s": null,
      "judge_s": 0.7325296710478142,
      "luna_s": null,
      "total_s": 2.6109320330433547,
      "writer_s": 1.8784023619955406
    }
  },
  {
    "case_id": "U27-e19",
    "record": {
      "comment_id": "U27-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "major": 0.98
              },
              "A1b": {
                "qg": 0.96
              },
              "B": {
                "point_0": 0.66
              },
              "B2": {}
            },
            "input_tokens": 2789,
            "latency_s": 1.000336,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.01,
                "question_or_guess": 0.98,
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
                  "close": 0.9400000000000001,
                  "hit": 0.77
                }
              },
              "B2": 1.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.77, 矛盾=1.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！ほかの可能性も考えながら、推理を続けてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "人生ゲームの車の駒を進めてるんだね。楽しんでるのは男だけで、妻と子どもは嫌々付き合わされてるのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.0006601789500564,
      "jev_s": null,
      "judge_s": 1.0006601789500564,
      "luna_s": null,
      "total_s": 2.885325278970413,
      "writer_s": 1.8846651000203565
    }
  },
  {
    "case_id": "U27-e20",
    "record": {
      "comment_id": "U27-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "kind": 0.77
              },
              "B": {
                "point_0": 1.0
              }
            },
            "guess_demoted": true,
            "input_tokens": 2045,
            "latency_s": 0.917175,
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
                "q_multi": 0.06,
                "q_open": 0.85,
                "q_yesno": 0.09
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
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。別の考え方でも考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "妻が運転していて、男は助手席から道案内をしてるだけなんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.9174980570096523,
      "jev_s": null,
      "judge_s": 0.9174980570096523,
      "luna_s": null,
      "total_s": 2.218153488007374,
      "writer_s": 1.3006554309977219
    }
  },
  {
    "case_id": "U27-e21",
    "record": {
      "comment_id": "U27-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "qg": 1.0
              },
              "A2": {
                "kind": 0.76
              },
              "B": {
                "point_0": 1.0
              }
            },
            "guess_demoted": true,
            "input_tokens": 2073,
            "latency_s": 0.935502,
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
                "guess": 1.0,
                "question": 0.0
              },
              "A2": {
                "q_multi": 0.04,
                "q_open": 0.84,
                "q_yesno": 0.12
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
      "shadow_mismatch": null,
      "text": "車型の遊園地の乗り物に家族で乗って、男が運転手役をしてるんだと思う。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.9358426469843835,
      "jev_s": null,
      "judge_s": 0.9358426469843835,
      "luna_s": null,
      "total_s": 2.241940845036879,
      "writer_s": 1.3060981980524957
    }
  },
  {
    "case_id": "U27-k01",
    "record": {
      "comment_id": "U27-k01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "point_0": 0.77
              },
              "B2": {}
            },
            "input_tokens": 2745,
            "latency_s": 0.889711,
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
                  "close": 0.94,
                  "hit": 0.85
                }
              },
              "B2": 0.06
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.85, 矛盾=0.06"
        },
        "jev": null,
        "luna": null
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
      "shadow_mismatch": null,
      "text": "車も家族も盤上のコマやピンで、男は人生ゲームの長い道を進めていたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.8899930419865996,
      "jev_s": null,
      "judge_s": 0.8899930419865996,
      "luna_s": null,
      "total_s": 0.8900090609677136,
      "writer_s": 1.6018981114029884e-05
    }
  },
  {
    "case_id": "U27-k02",
    "record": {
      "comment_id": "U27-k02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "major": 0.96
              },
              "A1b": {
                "qg": 0.92
              },
              "B": {
                "point_0": 0.97
              },
              "B2": {}
            },
            "input_tokens": 2737,
            "latency_s": 1.008295,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.01,
                "question_or_guess": 0.97,
                "reaction": 0.01,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.96,
                "question": 0.04
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.99,
                  "hit": 0.98
                }
              },
              "B2": 0.03
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.98, 矛盾=0.03"
        },
        "jev": null,
        "luna": null
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
      "shadow_mismatch": null,
      "text": "ゲームの車コマに家族を表すピンを挿して、人生ゲームで道を進んでいたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.0086254479829222,
      "jev_s": null,
      "judge_s": 1.0086254479829222,
      "luna_s": null,
      "total_s": 1.0086305770091712,
      "writer_s": 5.129026249051094e-06
    }
  },
  {
    "case_id": "U27-k03",
    "record": {
      "comment_id": "U27-k03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "qg": 0.96
              },
              "B": {
                "point_0": 0.73
              }
            },
            "input_tokens": 1747,
            "latency_s": 0.769428,
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
                  "close": 0.9199999999999999,
                  "hit": 0.1
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
          "reason": "段A=guess→guess_close, 要点最低=0.10"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "家族でボードゲームを囲み、車のおもちゃを盤の道に沿って進めていたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.7696619490161538,
      "jev_s": null,
      "judge_s": 0.7696619490161538,
      "luna_s": null,
      "total_s": 2.1032734669279307,
      "writer_s": 1.333611517911777
    }
  },
  {
    "case_id": "U27-k04",
    "record": {
      "comment_id": "U27-k04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "qg": 0.98
              },
              "B": {
                "point_0": 0.7
              }
            },
            "input_tokens": 1765,
            "latency_s": 0.698828,
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
                "guess": 0.99,
                "question": 0.01
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.9700000000000001,
                  "hit": 0.17
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
          "reason": "段A=guess→guess_close, 要点最低=0.17"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し推理を続けてみようか😌"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "すごろくの車コマを進めてたんだね。でも家族は一緒に楽しまず、男につき合ってるだけか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.6989915570011362,
      "jev_s": null,
      "judge_s": 0.6989915570011362,
      "luna_s": null,
      "total_s": 2.77861227595713,
      "writer_s": 2.0796207189559937
    }
  },
  {
    "case_id": "U27-k05",
    "record": {
      "comment_id": "U27-k05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "point_0": 0.6
              }
            },
            "input_tokens": 1717,
            "latency_s": 0.636459,
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
                  "close": 0.9299999999999999,
                  "hit": 0.2
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
          "reason": "段A=guess→guess_close, 要点最低=0.20"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "車は盤の上で動かす遊びのコマだったんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.6366033939411864,
      "jev_s": null,
      "judge_s": 0.6366033939411864,
      "luna_s": null,
      "total_s": 2.1206251749536023,
      "writer_s": 1.4840217810124159
    }
  },
  {
    "case_id": "U27-k06",
    "record": {
      "comment_id": "U27-k06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "qg": 0.92
              },
              "A2": {
                "kind": 0.67
              },
              "B": {
                "point_0": 0.99
              }
            },
            "guess_demoted": true,
            "input_tokens": 2057,
            "latency_s": 0.944374,
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
                "guess": 0.96,
                "question": 0.04
              },
              "A2": {
                "q_multi": 0.06,
                "q_open": 0.78,
                "q_yesno": 0.16
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.01,
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
          "reason": "段A=question→guess_wrong, 要点最低=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。別の可能性も考えてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "妻が本物の車を運転し、男は助手席から家族に道を教えてたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.9445643989602104,
      "jev_s": null,
      "judge_s": 0.9445643989602104,
      "luna_s": null,
      "total_s": 2.0567103669745848,
      "writer_s": 1.1121459680143744
    }
  },
  {
    "case_id": "U27-t01",
    "record": {
      "comment_id": "U27-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "3fa8694b418f",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": "人生ゲーム",
          "debug": {
            "calls": 1,
            "confidence": {
              "A1": {
                "major": 1.0
              }
            },
            "input_tokens": 776,
            "latency_s": 0.229873,
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
              "A_bare": 0.8
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.80"
        },
        "jev": null,
        "luna": null
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
      "shadow_mismatch": null,
      "text": "人生ゲーム？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.2300021779956296,
      "jev_s": null,
      "judge_s": 0.2300021779956296,
      "luna_s": null,
      "total_s": 4.058776708086953,
      "writer_s": 3.828774530091323
    }
  },
  {
    "case_id": "U27-t02",
    "record": {
      "comment_id": "U27-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "3fa8694b418f",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": "遊園地",
          "debug": {
            "calls": 1,
            "confidence": {
              "A1": {
                "major": 0.75
              }
            },
            "input_tokens": 776,
            "latency_s": 0.236503,
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.02,
                "question_or_guess": 0.8,
                "reaction": 0.18,
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
      "shadow_mismatch": null,
      "text": "遊園地",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.23664177302271128,
      "jev_s": null,
      "judge_s": 0.23664177302271128,
      "luna_s": null,
      "total_s": 2.892305147019215,
      "writer_s": 2.6556633739965037
    }
  },
  {
    "case_id": "c-ask_howto-03",
    "record": {
      "comment_id": "c-ask_howto-03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "major": 0.94
              },
              "A2": {
                "kind": 1.0
              }
            },
            "input_tokens": 1055,
            "latency_s": 0.443337,
            "major": "request",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.04,
                "reaction": 0.01,
                "request": 0.95
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
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "そうだよ！はい・いいえで答えられる質問をしてごらん。私が答えるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "はい・いいえで答えればいい感じ？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.44353050098288804,
      "jev_s": null,
      "judge_s": 0.44353050098288804,
      "luna_s": null,
      "total_s": 2.1868514999514446,
      "writer_s": 1.7433209989685565
    }
  },
  {
    "case_id": "c-cheer-02",
    "record": {
      "comment_id": "c-cheer-02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "cheer"
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
            "input_tokens": 1148,
            "latency_s": 0.457315,
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
                "cheer": 1.0,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.0,
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
          "kind": "cheer",
          "reason": "段A=reaction→cheer"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "応援ありがとう！うれしいよ☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "応援してます！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.4574924139305949,
      "jev_s": null,
      "judge_s": 0.4574924139305949,
      "luna_s": null,
      "total_s": 1.7039304468780756,
      "writer_s": 1.2464380329474807
    }
  },
  {
    "case_id": "c-complaint-01",
    "record": {
      "comment_id": "c-complaint-01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "complaint"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "confidence": {
              "A1": {
                "major": 0.93
              },
              "A2": {
                "kind": 0.87
              }
            },
            "input_tokens": 1158,
            "latency_s": 0.483424,
            "major": "reaction",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.05,
                "reaction": 0.94,
                "request": 0.01
              },
              "A2": {
                "chat": 0.0,
                "cheer": 0.01,
                "complaint": 0.89,
                "greeting": 0.0,
                "impression": 0.09,
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
          "kind": "complaint",
          "reason": "段A=reaction→complaint"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "教えてくれてありがとう。確認するね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "これちょっと説明足りなくない？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.4835511409910396,
      "jev_s": null,
      "judge_s": 0.4835511409910396,
      "luna_s": null,
      "total_s": 2.39321483601816,
      "writer_s": 1.9096636950271204
    }
  },
  {
    "case_id": "c-emoji_only-05",
    "record": {
      "comment_id": "c-emoji_only-05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "コメントありがとう！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "🕵️‍♂️❓",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 4.9005961045622826e-05,
      "jev_s": null,
      "judge_s": 4.9005961045622826e-05,
      "luna_s": null,
      "total_s": 3.132812667055987,
      "writer_s": 3.132763661094941
    }
  },
  {
    "case_id": "c-spam-04",
    "record": {
      "comment_id": "c-spam-04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
            "input_tokens": 1087,
            "latency_s": 0.458919,
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
      "shadow_mismatch": null,
      "text": "投資案件紹介中！DMください",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.45899840304628015,
      "jev_s": null,
      "judge_s": 0.45899840304628015,
      "luna_s": null,
      "total_s": 0.4590015570865944,
      "writer_s": 3.154040314257145e-06
    }
  },
  {
    "case_id": "c-abuse-08",
    "record": {
      "comment_id": "c-abuse-08",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "3fa8694b418f",
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
                "major": 0.93
              },
              "A2": {
                "kind": 1.0
              }
            },
            "input_tokens": 1101,
            "latency_s": 0.490219,
            "major": "inappropriate",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.94,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.01,
                "request": 0.05
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
      "shadow_mismatch": null,
      "text": "作者の顔写真あげてよ、脱いでるやつ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.4903262429870665,
      "jev_s": null,
      "judge_s": 0.4903262429870665,
      "luna_s": null,
      "total_s": 0.4903420259943232,
      "writer_s": 1.5783007256686687e-05
    }
  }
];
