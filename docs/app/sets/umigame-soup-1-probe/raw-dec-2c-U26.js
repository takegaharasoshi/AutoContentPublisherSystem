window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["dec-2c/U26"] = [
  {
    "case_id": "U26-e01",
    "record": {
      "comment_id": "U26-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "kind": 0.96
              },
              "B": {
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 1.0
              }
            },
            "input_tokens": 3286,
            "latency_s": 1.448337,
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
              "C": 0.56,
              "D": {
                "irrelevant": 0.0,
                "no": 0.0,
                "yes": 1.0
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
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "日本語を覚える前も、二人は毎日会話してたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.4487058320082724,
      "jev_s": null,
      "judge_s": 1.4487058320082724,
      "luna_s": null,
      "total_s": 2.6369409520411864,
      "writer_s": 1.188235120032914
    }
  },
  {
    "case_id": "U26-e02",
    "record": {
      "comment_id": "U26-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "qg": 0.72
              },
              "A2": {
                "kind": 0.99
              },
              "B": {
                "point_0": 0.61
              },
              "C": {}
            },
            "input_tokens": 2333,
            "latency_s": 1.157171,
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
                "guess": 0.86,
                "question": 0.14
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.26,
                  "hit": 0.01
                }
              },
              "C": 0.16
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 要点最低=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で、質問してみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "夫が間に入って通訳してた？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.1574980620061979,
      "jev_s": null,
      "judge_s": 1.1574980620061979,
      "luna_s": null,
      "total_s": 4.656503298901953,
      "writer_s": 3.499005236895755
    }
  },
  {
    "case_id": "U26-e03",
    "record": {
      "comment_id": "U26-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "qg": 0.26
              },
              "A2": {
                "kind": 0.99
              },
              "B": {
                "point_0": 0.89
              },
              "C": {}
            },
            "input_tokens": 2338,
            "latency_s": 1.192632,
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
                "guess": 0.63,
                "question": 0.37
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.06999999999999999,
                  "hit": 0.01
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
          "reason": "段A=question→q_open, 要点最低=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "誰が間に入って伝えてたのかも書いて、はい・いいえで答えられる質問にしてみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "間に入って伝えてたのは家族？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.1928716989932582,
      "jev_s": null,
      "judge_s": 1.1928716989932582,
      "luna_s": null,
      "total_s": 3.7620755449170247,
      "writer_s": 2.5692038459237665
    }
  },
  {
    "case_id": "U26-e04",
    "record": {
      "comment_id": "U26-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "qg": 0.48
              },
              "A2": {
                "kind": 0.96
              },
              "B": {
                "point_0": 1.0
              },
              "C": {}
            },
            "input_tokens": 2358,
            "latency_s": 1.12706,
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
                "guess": 0.26,
                "question": 0.74
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
              "C": 0.19
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
      "media_id": "local-U26",
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
      "text": "女は最近、辞書で日本語を勉強したの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.1273306990042329,
      "jev_s": null,
      "judge_s": 1.1273306990042329,
      "luna_s": null,
      "total_s": 4.914517991943285,
      "writer_s": 3.787187292939052
    }
  },
  {
    "case_id": "U26-e05",
    "record": {
      "comment_id": "U26-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "qg": 0.32
              },
              "A2": {
                "kind": 0.97
              },
              "B": {
                "point_0": 1.0
              },
              "C": {}
            },
            "input_tokens": 2348,
            "latency_s": 1.128871,
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
                "guess": 0.34,
                "question": 0.66
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
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "「義母の性格はこの10年で変わったの？」と聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "義母の性格がこの10年で変わった？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.129135743016377,
      "jev_s": null,
      "judge_s": 1.129135743016377,
      "luna_s": null,
      "total_s": 4.1743255039909855,
      "writer_s": 3.0451897609746084
    }
  },
  {
    "case_id": "U26-e06",
    "record": {
      "comment_id": "U26-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "qg": 0.24
              },
              "A2": {
                "kind": 0.96
              },
              "B": {
                "point_0": 0.94
              },
              "C": {}
            },
            "input_tokens": 2353,
            "latency_s": 1.592099,
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
                "guess": 0.62,
                "question": 0.38
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.02,
                "q_yesno": 0.97
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.04,
                  "hit": 0.01
                }
              },
              "C": 0.14
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 要点最低=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "近所の人が悪口を吹き込んだの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.5923925990937278,
      "jev_s": null,
      "judge_s": 1.5923925990937278,
      "luna_s": null,
      "total_s": 4.653936214046553,
      "writer_s": 3.061543614952825
    }
  },
  {
    "case_id": "U26-e07",
    "record": {
      "comment_id": "U26-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "point_0": 1.0
              },
              "C": {}
            },
            "input_tokens": 2353,
            "latency_s": 1.196468,
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
              "C": 0.13
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
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で、もう一度聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "二人は今も同じ家に住んでるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.1967800429556519,
      "jev_s": null,
      "judge_s": 1.1967800429556519,
      "luna_s": null,
      "total_s": 4.077926394995302,
      "writer_s": 2.88114635203965
    }
  },
  {
    "case_id": "U26-e08",
    "record": {
      "comment_id": "U26-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "qg": 0.8
              },
              "A2": {
                "kind": 0.94
              },
              "B": {
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.99
              }
            },
            "input_tokens": 3262,
            "latency_s": 1.492554,
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
                "guess": 0.1,
                "question": 0.9
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.03,
                "q_yesno": 0.96
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.23,
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
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
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
      "text": "言い合いの話題は料理とか家事だったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.49293548904825,
      "jev_s": null,
      "judge_s": 1.49293548904825,
      "luna_s": null,
      "total_s": 3.6278198841027915,
      "writer_s": 2.1348843950545415
    }
  },
  {
    "case_id": "U26-e09",
    "record": {
      "comment_id": "U26-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "kind": 0.94
              },
              "B": {
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.48
              }
            },
            "input_tokens": 3274,
            "latency_s": 1.381808,
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
                "q_open": 0.03,
                "q_yesno": 0.96
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.31,
              "D": {
                "irrelevant": 0.07,
                "no": 0.65,
                "yes": 0.28
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
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ほかのことも聞いてごらん"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "女がどこの国から来たかって、問題に関係ある？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.382160802022554,
      "jev_s": null,
      "judge_s": 1.382160802022554,
      "luna_s": null,
      "total_s": 3.0892780140275136,
      "writer_s": 1.7071172120049596
    }
  },
  {
    "case_id": "U26-e10",
    "record": {
      "comment_id": "U26-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "qg": 0.24
              },
              "A2": {
                "kind": 0.97
              },
              "B": {
                "point_0": 1.0
              },
              "C": {}
            },
            "input_tokens": 2338,
            "latency_s": 1.136953,
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
                "guess": 0.38,
                "question": 0.62
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
      "media_id": "local-U26",
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
      "text": "夫は仕事で遅く帰ってたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.1372234621085227,
      "jev_s": null,
      "judge_s": 1.1372234621085227,
      "luna_s": null,
      "total_s": 3.28042659512721,
      "writer_s": 2.1432031330186874
    }
  },
  {
    "case_id": "U26-e11",
    "record": {
      "comment_id": "U26-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "major": 0.98
              },
              "A1b": {
                "qg": 0.94
              },
              "A2": {
                "kind": 0.94
              }
            },
            "input_tokens": 1506,
            "latency_s": 0.674429,
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
                "guess": 0.03,
                "question": 0.97
              },
              "A2": {
                "q_multi": 0.96,
                "q_open": 0.03,
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
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。まずどっちから聞こうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "誰が二人の間で訳してたの？夫は家にいなかったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.6745631858939305,
      "jev_s": null,
      "judge_s": 0.6745631858939305,
      "luna_s": null,
      "total_s": 3.059480396914296,
      "writer_s": 2.3849172110203654
    }
  },
  {
    "case_id": "U26-e12",
    "record": {
      "comment_id": "U26-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "kind": 0.91
              }
            },
            "input_tokens": 1521,
            "latency_s": 0.865837,
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
                "q_multi": 0.94,
                "q_open": 0.04,
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
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。まずはどちらか聞いてごらん☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "日本語が話せるようになったのはいつ？二人は何のことで言い合ってたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.8660805330146104,
      "jev_s": null,
      "judge_s": 0.8660805330146104,
      "luna_s": null,
      "total_s": 3.0910932909464464,
      "writer_s": 2.225012757931836
    }
  },
  {
    "case_id": "U26-e13",
    "record": {
      "comment_id": "U26-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "qg": 0.8
              },
              "A2": {
                "kind": 0.97
              },
              "A3": {}
            },
            "input_tokens": 1883,
            "latency_s": 1.023154,
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
                "guess": 0.1,
                "question": 0.9
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.98,
                "q_yesno": 0.02
              },
              "A3": 0.03,
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.03"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
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
      "text": "なぜ日本語を覚えてから、二人は毎日けんかするようになったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.0234482049709186,
      "jev_s": null,
      "judge_s": 1.0234482049709186,
      "luna_s": null,
      "total_s": 2.7550140969688073,
      "writer_s": 1.7315658919978887
    }
  },
  {
    "case_id": "U26-e14",
    "record": {
      "comment_id": "U26-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "qg": 0.84
              },
              "A2": {
                "kind": 0.99
              },
              "A3": {}
            },
            "input_tokens": 1871,
            "latency_s": 0.913302,
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
                "guess": 0.08,
                "question": 0.92
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.99,
                "q_yesno": 0.01
              },
              "A3": 0.01,
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形に聞き直してみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "どうして二人は10年間も近所で仲がいいと思われていたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.9135633860714734,
      "jev_s": null,
      "judge_s": 0.9135633860714734,
      "luna_s": null,
      "total_s": 2.705781441065483,
      "writer_s": 1.7922180549940094
    }
  },
  {
    "case_id": "U26-e15",
    "record": {
      "comment_id": "U26-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "qg": 0.72
              },
              "A2": {
                "kind": 0.79
              },
              "A3": {}
            },
            "input_tokens": 1839,
            "latency_s": 0.886141,
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
                "guess": 0.14,
                "question": 0.86
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.86,
                "q_yesno": 0.13
              },
              "A3": 0.01,
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞き直してね。誰のことかも書いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "彼女はそれをいつから言ってたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.8863235099706799,
      "jev_s": null,
      "judge_s": 0.8863235099706799,
      "luna_s": null,
      "total_s": 2.713995946920477,
      "writer_s": 1.827672436949797
    }
  },
  {
    "case_id": "U26-e16",
    "record": {
      "comment_id": "U26-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "point_0": 0.97
              },
              "B2": {}
            },
            "input_tokens": 3032,
            "latency_s": 0.926339,
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
                  "close": 0.99,
                  "hit": 0.98
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
          "reason": "段A=guess→guess_correct, 要点最低=0.98, 矛盾=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！息子が嫁と義母の言葉を作り替えて通訳していた。女が日本語を覚えて本音が伝わり、けんかが始まった。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "息子が母と義母の通訳をしていたが、けんかを避けるため互いの不満をやさしい言葉に作り替えていた。息子が寮に入り、母が日本語を覚えて本音を直接聞くと、二人は言い合いを始め、通訳が作り話だったと気づいた。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.9265452900435776,
      "jev_s": null,
      "judge_s": 0.9265452900435776,
      "luna_s": null,
      "total_s": 0.9265646750573069,
      "writer_s": 1.9385013729333878e-05
    }
  },
  {
    "case_id": "U26-e17",
    "record": {
      "comment_id": "U26-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "qg": 0.98
              },
              "B": {
                "point_0": 0.66
              },
              "B2": {}
            },
            "input_tokens": 2888,
            "latency_s": 0.918866,
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
                  "close": 0.93,
                  "hit": 0.77
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
          "reason": "段A=guess→guess_correct, 要点最低=0.77, 矛盾=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！息子が嫁と義母の言葉を作り替えて通訳していた。女が日本語を覚えて本音が伝わり、けんかが始まった。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "息子が嫁と義母の言葉を仲直りのために作り替えて訳していた。日本語を覚えた嫁に本音が伝わり、けんかが始まった、ってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.9190663760527968,
      "jev_s": null,
      "judge_s": 0.9190663760527968,
      "luna_s": null,
      "total_s": 0.9190740850754082,
      "writer_s": 7.709022611379623e-06
    }
  },
  {
    "case_id": "U26-e18",
    "record": {
      "comment_id": "U26-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "point_0": 0.96
              }
            },
            "input_tokens": 1728,
            "latency_s": 0.707015,
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
                  "close": 0.99,
                  "hit": 0.02
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
          "reason": "段A=guess→guess_close, 要点最低=0.02"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！推理を続けてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "会話の間にいつも家族が入って訳していて、その人の伝え方が変わったんじゃない？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.7073434550547972,
      "jev_s": null,
      "judge_s": 0.7073434550547972,
      "luna_s": null,
      "total_s": 2.522341821109876,
      "writer_s": 1.8149983660550788
    }
  },
  {
    "case_id": "U26-e19",
    "record": {
      "comment_id": "U26-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "point_0": 1.0
              }
            },
            "input_tokens": 1722,
            "latency_s": 0.679429,
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
                  "close": 1.0,
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
      "media_id": "local-U26",
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
      "text": "誰かが2人の言葉をわざと良い言葉に変えて伝えてたんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.6795914869289845,
      "jev_s": null,
      "judge_s": 0.6795914869289845,
      "luna_s": null,
      "total_s": 2.8089603278785944,
      "writer_s": 2.12936884094961
    }
  },
  {
    "case_id": "U26-e20",
    "record": {
      "comment_id": "U26-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "major": 0.95
              },
              "A1b": {
                "qg": 0.96
              },
              "A2": {
                "kind": 0.73
              },
              "B": {
                "point_0": 1.0
              }
            },
            "guess_demoted": true,
            "input_tokens": 2058,
            "latency_s": 0.88752,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.96,
                "reaction": 0.02,
                "request": 0.02
              },
              "A1b": {
                "guess": 0.98,
                "question": 0.02
              },
              "A2": {
                "q_multi": 0.05,
                "q_open": 0.82,
                "q_yesno": 0.13
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
      "media_id": "local-U26",
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
      "text": "義母がこの10年で急に意地悪になり、嫁が腹を立てたから毎日けんかしたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.8878017840906978,
      "jev_s": null,
      "judge_s": 0.8878017840906978,
      "luna_s": null,
      "total_s": 3.1927659251959994,
      "writer_s": 2.3049641411053017
    }
  },
  {
    "case_id": "U26-e21",
    "record": {
      "comment_id": "U26-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "qg": 0.9
              },
              "A2": {
                "kind": 0.72
              },
              "B": {
                "point_0": 0.99
              }
            },
            "guess_demoted": true,
            "input_tokens": 2030,
            "latency_s": 0.871301,
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
                "guess": 0.95,
                "question": 0.05
              },
              "A2": {
                "q_multi": 0.04,
                "q_open": 0.81,
                "q_yesno": 0.15
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
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
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
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
      "text": "近所の人が二人の間で嘘を吹き込み、仲を悪くしたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.8715981870191172,
      "jev_s": null,
      "judge_s": 0.8715981870191172,
      "luna_s": null,
      "total_s": 3.7301205949625,
      "writer_s": 2.858522407943383
    }
  },
  {
    "case_id": "U26-b22",
    "record": {
      "comment_id": "U26-b22",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.67
              }
            },
            "input_tokens": 3268,
            "latency_s": 1.775881,
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
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.86,
              "D": {
                "irrelevant": 0.15,
                "no": 0.07,
                "yes": 0.78
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
      "media_id": "local-U26",
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
      "text": "義母は日本語以外の言葉を話してたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.7762995579978451,
      "jev_s": null,
      "judge_s": 1.7762995579978451,
      "luna_s": null,
      "total_s": 3.663421973004006,
      "writer_s": 1.8871224150061607
    }
  },
  {
    "case_id": "U26-b23",
    "record": {
      "comment_id": "U26-b23",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 1.0
              }
            },
            "input_tokens": 3250,
            "latency_s": 1.371297,
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
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.88,
              "D": {
                "irrelevant": 0.0,
                "no": 0.0,
                "yes": 1.0
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
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！その調子で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "2人は同じ家に住んでたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.3716565100476146,
      "jev_s": null,
      "judge_s": 1.3716565100476146,
      "luna_s": null,
      "total_s": 3.1662460770457983,
      "writer_s": 1.7945895669981837
    }
  },
  {
    "case_id": "U26-b24",
    "record": {
      "comment_id": "U26-b24",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "kind": 1.0
              },
              "B": {
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.45
              }
            },
            "input_tokens": 3220,
            "latency_s": 1.472327,
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
              "C": 0.44,
              "D": {
                "irrelevant": 0.26,
                "no": 0.11,
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
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "義母も外国出身なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.4727417139802128,
      "jev_s": null,
      "judge_s": 1.4727417139802128,
      "luna_s": null,
      "total_s": 2.6921549850376323,
      "writer_s": 1.2194132710574195
    }
  },
  {
    "case_id": "U26-b25",
    "record": {
      "comment_id": "U26-b25",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "qg": 1.0
              },
              "A2": {
                "kind": 0.96
              },
              "B": {
                "point_0": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.48
              }
            },
            "input_tokens": 3244,
            "latency_s": 1.589498,
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
              "C": 0.44,
              "D": {
                "irrelevant": 0.01,
                "no": 0.34,
                "yes": 0.65
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
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！夫はけんかに関係してるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "夫はけんかに関係してるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.5898382109589875,
      "jev_s": null,
      "judge_s": 1.5898382109589875,
      "luna_s": null,
      "total_s": 4.2645204439759254,
      "writer_s": 2.674682233016938
    }
  },
  {
    "case_id": "U26-k01",
    "record": {
      "comment_id": "U26-k01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "qg": 0.96
              },
              "B": {
                "point_0": 0.91
              },
              "B2": {}
            },
            "input_tokens": 2832,
            "latency_s": 0.910799,
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
                  "close": 0.99,
                  "hit": 0.94
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
          "reason": "段A=guess→guess_correct, 要点最低=0.94, 矛盾=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！息子が嫁と義母の言葉を作り替えて通訳していた。女が日本語を覚えて本音が伝わり、けんかが始まった。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "二人の会話を仲立ちした息子が、互いの不満を角の立たない言葉に直して伝えてたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.9110891879536211,
      "jev_s": null,
      "judge_s": 0.9110891879536211,
      "luna_s": null,
      "total_s": 0.9110943339765072,
      "writer_s": 5.1460228860378265e-06
    }
  },
  {
    "case_id": "U26-k02",
    "record": {
      "comment_id": "U26-k02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "qg": 0.98
              },
              "B": {
                "point_0": 0.89
              },
              "B2": {}
            },
            "input_tokens": 2816,
            "latency_s": 1.050162,
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
                "guess": 0.99,
                "question": 0.01
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.9800000000000001,
                  "hit": 0.93
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
          "reason": "段A=guess→guess_correct, 要点最低=0.93, 矛盾=0.06"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！息子が嫁と義母の言葉を作り替えて通訳していた。女が日本語を覚えて本音が伝わり、けんかが始まった。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "息子が母と祖母の間で、きつい言葉を気遣いのある表現に仕立てていたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.050608711084351,
      "jev_s": null,
      "judge_s": 1.050608711084351,
      "luna_s": null,
      "total_s": 1.050610859063454,
      "writer_s": 2.1479791030287743e-06
    }
  },
  {
    "case_id": "U26-k03",
    "record": {
      "comment_id": "U26-k03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "point_0": 0.96
              }
            },
            "input_tokens": 1734,
            "latency_s": 0.676374,
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
                  "close": 0.99,
                  "hit": 0.02
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
          "reason": "段A=guess→guess_close, 要点最低=0.02"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！推理を続けてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "家族の誰かがいつも通訳していて、その訳し方が二人の関係に影響してたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.6766226770123467,
      "jev_s": null,
      "judge_s": 0.6766226770123467,
      "luna_s": null,
      "total_s": 3.745252872002311,
      "writer_s": 3.0686301949899644
    }
  },
  {
    "case_id": "U26-k04",
    "record": {
      "comment_id": "U26-k04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "major": 0.87
              },
              "A1b": {
                "qg": 0.98
              },
              "B": {
                "point_0": 0.48
              },
              "B2": {}
            },
            "input_tokens": 2800,
            "latency_s": 0.935237,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.9,
                "reaction": 0.1,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.99,
                "question": 0.01
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.99,
                  "hit": 0.65
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
          "reason": "段A=guess→guess_correct, 要点最低=0.65, 矛盾=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！息子が嫁と義母の言葉を作り替えて通訳していた。女が日本語を覚えて本音が伝わり、けんかが始まった。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "息子が間で訳してたけど、言葉を少し足したり省いたりして伝えていたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.9354982529766858,
      "jev_s": null,
      "judge_s": 0.9354982529766858,
      "luna_s": null,
      "total_s": 0.9355110740289092,
      "writer_s": 1.2821052223443985e-05
    }
  },
  {
    "case_id": "U26-k05",
    "record": {
      "comment_id": "U26-k05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "qg": 1.0
              },
              "B": {
                "point_0": 0.99
              }
            },
            "input_tokens": 1737,
            "latency_s": 0.699053,
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
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
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
      "shadow_mismatch": null,
      "text": "二人の話はいつも誰かを通して届いていて、言葉の伝わり方に問題があったんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.6992969359271228,
      "jev_s": null,
      "judge_s": 0.6992969359271228,
      "luna_s": null,
      "total_s": 2.989564171875827,
      "writer_s": 2.290267235948704
    }
  },
  {
    "case_id": "U26-k06",
    "record": {
      "comment_id": "U26-k06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "kind": 0.72
              },
              "B": {
                "point_0": 1.0
              }
            },
            "guess_demoted": true,
            "input_tokens": 2058,
            "latency_s": 0.970182,
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
                "q_multi": 0.04,
                "q_open": 0.81,
                "q_yesno": 0.15
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
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "近所の人が義母の悪口を嫁に告げ、嫁はそれを聞いて義母とけんかしたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.9704651560168713,
      "jev_s": null,
      "judge_s": 0.9704651560168713,
      "luna_s": null,
      "total_s": 4.927122356952168,
      "writer_s": 3.9566572009352967
    }
  },
  {
    "case_id": "U26-t01",
    "record": {
      "comment_id": "U26-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "qg": 0.82
              },
              "A2": {
                "kind": 0.38
              },
              "B": {
                "point_0": 0.96
              },
              "C": {}
            },
            "input_tokens": 2308,
            "latency_s": 1.16469,
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
                "guess": 0.91,
                "question": 0.09
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.4,
                "q_yesno": 0.59
              },
              "A_bare": 0.15,
              "B": {
                "point_0": {
                  "close": 0.03,
                  "hit": 0.01
                }
              },
              "C": 0.01
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 要点最低=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "誰が息子の通訳なのか、はい・いいえで答えられる形で聞いてみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "息子の通訳？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.1649912290740758,
      "jev_s": null,
      "judge_s": 1.1649912290740758,
      "luna_s": null,
      "total_s": 3.7041592691093683,
      "writer_s": 2.5391680400352925
    }
  },
  {
    "case_id": "U26-t02",
    "record": {
      "comment_id": "U26-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "cb5eb45c4241",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": "富士山",
          "debug": {
            "calls": 1,
            "confidence": {
              "A1": {
                "major": 0.95
              }
            },
            "input_tokens": 776,
            "latency_s": 0.232816,
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.96,
                "reaction": 0.04,
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
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "富士山が何のことか、もう少し詳しく教えて！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "富士山",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.2331103109754622,
      "jev_s": null,
      "judge_s": 0.2331103109754622,
      "luna_s": null,
      "total_s": 4.032009394024499,
      "writer_s": 3.7988990830490366
    }
  },
  {
    "case_id": "c-ask_howto-02",
    "record": {
      "comment_id": "c-ask_howto-02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "major": 0.79
              },
              "A2": {
                "kind": 1.0
              }
            },
            "input_tokens": 1049,
            "latency_s": 0.455694,
            "major": "request",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.01,
                "other": 0.01,
                "question_or_guess": 0.08,
                "reaction": 0.07,
                "request": 0.83
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
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる質問をコメントしてごらん。私が答えるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "何をコメントしたらいいの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.45589582808315754,
      "jev_s": null,
      "judge_s": 0.45589582808315754,
      "luna_s": null,
      "total_s": 3.621393052046187,
      "writer_s": 3.1654972239630297
    }
  },
  {
    "case_id": "c-cheer-01",
    "record": {
      "comment_id": "c-cheer-01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "kind": 0.51
              }
            },
            "input_tokens": 1158,
            "latency_s": 0.512451,
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
                "chat": 0.03,
                "cheer": 0.58,
                "complaint": 0.0,
                "greeting": 0.32,
                "impression": 0.06,
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
          "kind": "cheer",
          "reason": "段A=reaction→cheer"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ありがとう！読んでくれてうれしいよ☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "今日も投稿おつかれさま！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.5126029909588397,
      "jev_s": null,
      "judge_s": 0.5126029909588397,
      "luna_s": null,
      "total_s": 2.131401564925909,
      "writer_s": 1.6187985739670694
    }
  },
  {
    "case_id": "c-request-05",
    "record": {
      "comment_id": "c-request-05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "request"
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
            "latency_s": 0.425041,
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
                "chat": 0.01,
                "cheer": 0.0,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.01,
                "mention": 0.0,
                "request": 0.98
              },
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "request",
          "reason": "段A=reaction→request"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "リクエストありがとう！参考にするね"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "次は家族もの出してほしいな",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.42514924600254744,
      "jev_s": null,
      "judge_s": 0.42514924600254744,
      "luna_s": null,
      "total_s": 2.7823815650772303,
      "writer_s": 2.357232319074683
    }
  },
  {
    "case_id": "c-emoji_only-04",
    "record": {
      "comment_id": "c-emoji_only-04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
      "media_id": "local-U26",
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
      "shadow_mismatch": null,
      "text": "👍✨",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 1.5308032743632793e-05,
      "jev_s": null,
      "judge_s": 1.5308032743632793e-05,
      "luna_s": null,
      "total_s": 1.4223021250218153,
      "writer_s": 1.4222868169890717
    }
  },
  {
    "case_id": "c-spam-03",
    "record": {
      "comment_id": "c-spam-03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 1097,
            "latency_s": 0.447751,
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
      "media_id": "local-U26",
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
      "text": "副業に興味ある人はプロフのリンクへ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.4479101069737226,
      "jev_s": null,
      "judge_s": 0.4479101069737226,
      "luna_s": null,
      "total_s": 0.44791368895675987,
      "writer_s": 3.5819830372929573e-06
    }
  },
  {
    "case_id": "c-abuse-07",
    "record": {
      "comment_id": "c-abuse-07",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
                "major": 0.77
              },
              "A2": {
                "kind": 0.99
              }
            },
            "input_tokens": 1097,
            "latency_s": 0.463417,
            "major": "inappropriate",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.82,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.18,
                "request": 0.0
              },
              "A2": {
                "abuse": 0.99,
                "personal_info": 0.0,
                "spam": 0.0,
                "troll": 0.01
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
      "media_id": "local-U26",
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
      "text": "ここでコメントしてる奴ら全員頭おかしい",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "decisions_s": 0.4635080919833854,
      "jev_s": null,
      "judge_s": 0.4635080919833854,
      "luna_s": null,
      "total_s": 0.4635265340330079,
      "writer_s": 1.8442049622535706e-05
    }
  }
];
