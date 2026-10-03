window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["luna-1d/U27"] = [
  {
    "case_id": "U27-e01",
    "record": {
      "comment_id": "U27-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": "no",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 240,
            "finish_reason": "stop",
            "latency_s": 3.628991,
            "model": "gpt-6-luna",
            "prompt_tokens": 3022,
            "reasoning_tokens": 162
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "一問のはい・いいえ質問。本物の車ではなく、家の中で動かしています。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。次はどんなことを聞こうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は本物の車を公道で運転しているんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 3.629027146002045,
      "luna_s": 3.629027146002045,
      "total_s": 5.018222804996185,
      "writer_s": 1.38919565899414
    }
  },
  {
    "case_id": "U27-e02",
    "record": {
      "comment_id": "U27-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": "no",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 353,
            "finish_reason": "stop",
            "latency_s": 4.656333,
            "model": "gpt-6-luna",
            "prompt_tokens": 3024,
            "reasoning_tokens": 283
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "妻や子どもたちは運転席にいる人ではありません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。妻や子どもたちの誰かが運転席にいるんですか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "妻や子どもたちの誰かが運転席にいるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 4.656387873983476,
      "luna_s": 4.656387873983476,
      "total_s": 6.899305911007104,
      "writer_s": 2.242918037023628
    }
  },
  {
    "case_id": "U27-e03",
    "record": {
      "comment_id": "U27-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": "no",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 305,
            "finish_reason": "stop",
            "latency_s": 3.894075,
            "model": "gpt-6-luna",
            "prompt_tokens": 3015,
            "reasoning_tokens": 232
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実では、車は自動運転ではなく男自身が動かしています。"
        }
      },
      "media_id": "local-U27",
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
      "shadow_mismatch": null,
      "text": "車は自動運転の車ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 3.894130959000904,
      "luna_s": 3.894130959000904,
      "total_s": 5.080228537990479,
      "writer_s": 1.1860975789895747
    }
  },
  {
    "case_id": "U27-e04",
    "record": {
      "comment_id": "U27-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": "no",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 519,
            "finish_reason": "stop",
            "latency_s": 5.660789,
            "model": "gpt-6-luna",
            "prompt_tokens": 3028,
            "reasoning_tokens": 442
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "男は本物の自動車を運転しておらず、運転経験があるとはいえません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ほかのことも聞いてごらん"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は運転免許を持っていないだけで、運転の経験はあるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 5.6608175080036744,
      "luna_s": 5.6608175080036744,
      "total_s": 7.0175777960103005,
      "writer_s": 1.356760288006626
    }
  },
  {
    "case_id": "U27-e05",
    "record": {
      "comment_id": "U27-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": "no",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 472,
            "finish_reason": "stop",
            "latency_s": 5.270501,
            "model": "gpt-6-luna",
            "prompt_tokens": 3024,
            "reasoning_tokens": 391
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "実際の車内移動ではなく、家族は遊びそのものを楽しんでいます。"
        }
      },
      "media_id": "local-U27",
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
      "shadow_mismatch": null,
      "text": "家族は車の中で移動そのものを楽しんでるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 5.270539667981211,
      "luna_s": 5.270539667981211,
      "total_s": 6.53083761796006,
      "writer_s": 1.260297949978849
    }
  },
  {
    "case_id": "U27-e06",
    "record": {
      "comment_id": "U27-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": "no",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 242,
            "finish_reason": "stop",
            "latency_s": 3.343833,
            "model": "gpt-6-luna",
            "prompt_tokens": 3022,
            "reasoning_tokens": 174
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実では家の中を走り、遊園地などの施設内ではありません。"
        }
      },
      "media_id": "local-U27",
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
      "shadow_mismatch": null,
      "text": "この車は遊園地などの施設の中を走るものですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 3.34385866401135,
      "luna_s": 3.34385866401135,
      "total_s": 4.489757375034969,
      "writer_s": 1.1458987110236194
    }
  },
  {
    "case_id": "U27-e07",
    "record": {
      "comment_id": "U27-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": "yes",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 241,
            "finish_reason": "stop",
            "latency_s": 3.729,
            "model": "gpt-6-luna",
            "prompt_tokens": 3020,
            "reasoning_tokens": 175
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、男は車の外から動かしているとあります。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
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
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 3.7290537930093706,
      "luna_s": 3.7290537930093706,
      "total_s": 6.418129402009072,
      "writer_s": 2.689075608999701
    }
  },
  {
    "case_id": "U27-e08",
    "record": {
      "comment_id": "U27-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": "irrelevant",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "completion_tokens": 439,
            "finish_reason": "stop",
            "latency_s": 5.070718,
            "model": "gpt-6-luna",
            "prompt_tokens": 3025,
            "reasoning_tokens": 364
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "移動にかかる時間は真相・確定事実に示されていません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "家族は長い距離を何時間もかけて移動するんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 5.070750876009697,
      "luna_s": 5.070750876009697,
      "total_s": 6.715592495020246,
      "writer_s": 1.644841619010549
    }
  },
  {
    "case_id": "U27-e09",
    "record": {
      "comment_id": "U27-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": "no",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 266,
            "finish_reason": "stop",
            "latency_s": 3.937441,
            "model": "gpt-6-luna",
            "prompt_tokens": 3019,
            "reasoning_tokens": 194
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "真相では本物の自動車ではないため、ガソリンで走る車ではありません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
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
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 3.937495696998667,
      "luna_s": 3.937495696998667,
      "total_s": 6.083185831987066,
      "writer_s": 2.1456901349883992
    }
  },
  {
    "case_id": "U27-e10",
    "record": {
      "comment_id": "U27-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": "no",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 221,
            "finish_reason": "stop",
            "latency_s": 2.724384,
            "model": "gpt-6-luna",
            "prompt_tokens": 3020,
            "reasoning_tokens": 136
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "ハンドルを握って操作しているかを尋ねる一問。車の外から動かしているため、いいえ。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。自分でハンドルを操作してるんですか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は自分でハンドルを操作してるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.72443216398824,
      "luna_s": 2.72443216398824,
      "total_s": 5.800324815005297,
      "writer_s": 3.075892651017057
    }
  },
  {
    "case_id": "U27-e11",
    "record": {
      "comment_id": "U27-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_multi"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 163,
            "finish_reason": "stop",
            "latency_s": 2.274668,
            "model": "gpt-6-luna",
            "prompt_tokens": 3029,
            "reasoning_tokens": 83
          },
          "error": null,
          "kind": "q_multi",
          "reason": "一つのコメントに、道路を走るかと誰が運転するかの質問が二つあります。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつ聞いてごらん。私が答えるよ☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "車は実際に道路を走ってるの？男以外の誰かが運転してるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.274733347003348,
      "luna_s": 2.274733347003348,
      "total_s": 4.911867780989269,
      "writer_s": 2.6371344339859206
    }
  },
  {
    "case_id": "U27-e12",
    "record": {
      "comment_id": "U27-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_multi"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 163,
            "finish_reason": "stop",
            "latency_s": 2.337661,
            "model": "gpt-6-luna",
            "prompt_tokens": 3027,
            "reasoning_tokens": 83
          },
          "error": null,
          "kind": "q_multi",
          "reason": "はい・いいえで答えられる質問が二つ含まれています。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつ聞いてごらん。どっちからいこうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "これは遊園地の乗り物なの？家族は運転ごっこをしてるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.3377162599936128,
      "luna_s": 2.3377162599936128,
      "total_s": 5.033416560996557,
      "writer_s": 2.695700301002944
    }
  },
  {
    "case_id": "U27-e13",
    "record": {
      "comment_id": "U27-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 177,
            "finish_reason": "stop",
            "latency_s": 2.969357,
            "model": "gpt-6-luna",
            "prompt_tokens": 3025,
            "reasoning_tokens": 94
          },
          "error": null,
          "kind": "q_open",
          "reason": "「どうやって」と尋ねる、はい／いいえでは答えられない質問です。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "「免許がない男は車を走らせているの？」みたいに、はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "免許がない男は、どうやって車を走らせているんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.969384010997601,
      "luna_s": 2.969384010997601,
      "total_s": 5.709757061005803,
      "writer_s": 2.740373050008202
    }
  },
  {
    "case_id": "U27-e14",
    "record": {
      "comment_id": "U27-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 245,
            "finish_reason": "stop",
            "latency_s": 3.151411,
            "model": "gpt-6-luna",
            "prompt_tokens": 3023,
            "reasoning_tokens": 166
          },
          "error": null,
          "kind": "q_open",
          "reason": "「誰の運転か」は、はい／いいえで答えられない質問です。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "妻と子どもたちが誰の運転で移動しているのか、はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "妻と子どもたちは誰の運転で移動しているんでしょう？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 3.1514736440149136,
      "luna_s": 3.1514736440149136,
      "total_s": 7.452280569035793,
      "writer_s": 4.300806925020879
    }
  },
  {
    "case_id": "U27-e15",
    "record": {
      "comment_id": "U27-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 186,
            "finish_reason": "stop",
            "latency_s": 2.822651,
            "model": "gpt-6-luna",
            "prompt_tokens": 3024,
            "reasoning_tokens": 102
          },
          "error": null,
          "kind": "q_open",
          "reason": "「どこからどこまで」は場所を尋ねる質問で、はい・いいえでは答えられません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "「長い道のり」はどこからどこまでか、はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "「長い道のり」とは、どこからどこまでのことですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.8226777180097997,
      "luna_s": 2.8226777180097997,
      "total_s": 5.649488206021488,
      "writer_s": 2.826810488011688
    }
  },
  {
    "case_id": "U27-e16",
    "record": {
      "comment_id": "U27-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_correct"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 291,
            "finish_reason": "stop",
            "latency_s": 3.462537,
            "model": "gpt-6-luna",
            "prompt_tokens": 3019,
            "reasoning_tokens": 191
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "人生ゲームの車の駒を動かしたという核心を言い当てています。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！男が走らせているのは人生ゲームの車の駒。妻と子どもはピンで乗せていて、おもちゃなので免許はいらない。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "人生ゲームの車の駒を動かしてたってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 3.4625973280053586,
      "luna_s": 3.4625973280053586,
      "total_s": 3.46261473101913,
      "writer_s": 1.7403013771399856e-05
    }
  },
  {
    "case_id": "U27-e17",
    "record": {
      "comment_id": "U27-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_correct"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 223,
            "finish_reason": "stop",
            "latency_s": 2.776234,
            "model": "gpt-6-luna",
            "prompt_tokens": 3045,
            "reasoning_tokens": 115
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "人生ゲームの車の駒を動かしていたという核心を言い当てています。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
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
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.7762964249996003,
      "luna_s": 2.7762964249996003,
      "total_s": 2.776303738995921,
      "writer_s": 7.313996320590377e-06
    }
  },
  {
    "case_id": "U27-e18",
    "record": {
      "comment_id": "U27-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_close"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 182,
            "finish_reason": "stop",
            "latency_s": 2.439764,
            "model": "gpt-6-luna",
            "prompt_tokens": 3037,
            "reasoning_tokens": 116
          },
          "error": null,
          "kind": "guess_close",
          "reason": "すごろくの車の駒という核心には触れていますが、人生ゲームとは特定できていません。"
        }
      },
      "media_id": "local-U27",
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
      "shadow_mismatch": null,
      "text": "家族で何かのすごろくをしていて、車の駒を長い道に沿って進めてるんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.439818931015907,
      "luna_s": 2.439818931015907,
      "total_s": 4.491979295009514,
      "writer_s": 2.0521603639936075
    }
  },
  {
    "case_id": "U27-e19",
    "record": {
      "comment_id": "U27-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_close"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 213,
            "finish_reason": "stop",
            "latency_s": 2.931571,
            "model": "gpt-6-luna",
            "prompt_tokens": 3047,
            "reasoning_tokens": 149
          },
          "error": null,
          "kind": "guess_close",
          "reason": "人生ゲームの車の駒には触れていますが、家族の楽しみ方に誤りがあります。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！推理を続けてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "人生ゲームの車の駒を進めてるんだね。楽しんでるのは男だけで、妻と子どもは嫌々付き合わされてるのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.9316277990001254,
      "luna_s": 2.9316277990001254,
      "total_s": 5.723538499994902,
      "writer_s": 2.7919107009947766
    }
  },
  {
    "case_id": "U27-e20",
    "record": {
      "comment_id": "U27-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_wrong"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 170,
            "finish_reason": "stop",
            "latency_s": 2.517791,
            "model": "gpt-6-luna",
            "prompt_tokens": 3028,
            "reasoning_tokens": 98
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "妻が運転し男が道案内をするという推理で、人生ゲームの車の駒には触れていません。"
        }
      },
      "media_id": "local-U27",
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
      "shadow_mismatch": null,
      "text": "妻が運転していて、男は助手席から道案内をしてるだけなんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.517842560017016,
      "luna_s": 2.517842560017016,
      "total_s": 3.52661805000389,
      "writer_s": 1.0087754899868742
    }
  },
  {
    "case_id": "U27-e21",
    "record": {
      "comment_id": "U27-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_wrong"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 326,
            "finish_reason": "stop",
            "latency_s": 3.892739,
            "model": "gpt-6-luna",
            "prompt_tokens": 3035,
            "reasoning_tokens": 246
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "遊園地の乗り物という推理で、人生ゲームの車の駒には触れていません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。もう少し考えてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "車型の遊園地の乗り物に家族で乗って、男が運転手役をしてるんだと思う。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 3.8928018410224468,
      "luna_s": 3.8928018410224468,
      "total_s": 4.929833880014485,
      "writer_s": 1.037032038992038
    }
  },
  {
    "case_id": "U27-t01",
    "record": {
      "comment_id": "U27-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": "人生ゲーム",
          "debug": {
            "completion_tokens": 169,
            "finish_reason": "stop",
            "latency_s": 2.492442,
            "model": "gpt-6-luna",
            "prompt_tokens": 3007,
            "reasoning_tokens": 94
          },
          "error": null,
          "kind": "q_open",
          "reason": "語句だけのコメントは、推理ではなく q_open として扱います。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
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
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.4924973959859926,
      "luna_s": 2.4924973959859926,
      "total_s": 7.0260798369999975,
      "writer_s": 4.533582441014005
    }
  },
  {
    "case_id": "U27-t02",
    "record": {
      "comment_id": "U27-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": "遊園地",
          "debug": {
            "completion_tokens": 248,
            "finish_reason": "stop",
            "latency_s": 2.898019,
            "model": "gpt-6-luna",
            "prompt_tokens": 3007,
            "reasoning_tokens": 156
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句だけのコメントなので、はい／いいえで答えられない質問として扱います。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
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
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.8980475300049875,
      "luna_s": 2.8980475300049875,
      "total_s": 6.987017692008521,
      "writer_s": 4.088970162003534
    }
  },
  {
    "case_id": "c-ask_howto-03",
    "record": {
      "comment_id": "c-ask_howto-03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "ask_howto"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 131,
            "finish_reason": "stop",
            "latency_s": 1.951294,
            "model": "gpt-6-luna",
            "prompt_tokens": 3015,
            "reasoning_tokens": 56
          },
          "error": null,
          "kind": "ask_howto",
          "reason": "遊び方として、質問の答え方を尋ねています。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
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
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 1.951352243020665,
      "luna_s": 1.951352243020665,
      "total_s": 4.207648557028733,
      "writer_s": 2.2562963140080683
    }
  },
  {
    "case_id": "c-cheer-02",
    "record": {
      "comment_id": "c-cheer-02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "cheer"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 95,
            "finish_reason": "stop",
            "latency_s": 1.780225,
            "model": "gpt-6-luna",
            "prompt_tokens": 3009,
            "reasoning_tokens": 34
          },
          "error": null,
          "kind": "cheer",
          "reason": "応援の言葉なので、励ましへのお礼を返します。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "応援ありがとう！一緒に楽しんでいこうね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "応援してます！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 1.7802822350058705,
      "luna_s": 1.7802822350058705,
      "total_s": 3.103530819993466,
      "writer_s": 1.3232485849875957
    }
  },
  {
    "case_id": "c-complaint-01",
    "record": {
      "comment_id": "c-complaint-01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "complaint"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 139,
            "finish_reason": "stop",
            "latency_s": 2.070141,
            "model": "gpt-6-luna",
            "prompt_tokens": 3014,
            "reasoning_tokens": 75
          },
          "error": null,
          "kind": "complaint",
          "reason": "問題の説明が足りないという指摘のため、クレームに分類します。"
        }
      },
      "media_id": "local-U27",
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
      "shadow_mismatch": null,
      "text": "これちょっと説明足りなくない？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.0701989730005153,
      "luna_s": 2.0701989730005153,
      "total_s": 4.004044604982482,
      "writer_s": 1.933845631981967
    }
  },
  {
    "case_id": "c-emoji_only-05",
    "record": {
      "comment_id": "c-emoji_only-05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "emoji_only"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 91,
            "finish_reason": "stop",
            "latency_s": 1.89238,
            "model": "gpt-6-luna",
            "prompt_tokens": 3013,
            "reasoning_tokens": 37
          },
          "error": null,
          "kind": "emoji_only",
          "reason": "絵文字だけのコメントなので、emoji_onlyに分類します。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
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
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 1.8924330320151057,
      "luna_s": 1.8924330320151057,
      "total_s": 3.667348484013928,
      "writer_s": 1.7749154519988224
    }
  },
  {
    "case_id": "c-spam-04",
    "record": {
      "comment_id": "c-spam-04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "spam"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 90,
            "finish_reason": "stop",
            "latency_s": 1.737962,
            "model": "gpt-6-luna",
            "prompt_tokens": 3012,
            "reasoning_tokens": 40
          },
          "error": null,
          "kind": "spam",
          "reason": "投資案件を宣伝し、DMへ誘導しているため。"
        }
      },
      "media_id": "local-U27",
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
      "text": "投資案件紹介中！DMください",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 1.7380289130087476,
      "luna_s": 1.7380289130087476,
      "total_s": 1.7380368770100176,
      "writer_s": 7.964001270011067e-06
    }
  },
  {
    "case_id": "c-abuse-08",
    "record": {
      "comment_id": "c-abuse-08",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "luna",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": false
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "abuse"
      },
      "judgements": {
        "jev": null,
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 141,
            "finish_reason": "stop",
            "latency_s": 2.328618,
            "model": "gpt-6-luna",
            "prompt_tokens": 3019,
            "reasoning_tokens": 92
          },
          "error": null,
          "kind": "abuse",
          "reason": "作者に裸の写真を求める性的な内容のため"
        }
      },
      "media_id": "local-U27",
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
      "shadow_mismatch": null,
      "text": "作者の顔写真あげてよ、脱いでるやつ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": null,
      "judge_s": 2.328666474990314,
      "luna_s": 2.328666474990314,
      "total_s": 2.328672153991647,
      "writer_s": 5.679001333191991e-06
    }
  }
];
