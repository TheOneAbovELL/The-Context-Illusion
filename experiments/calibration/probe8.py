"""After the elimination shortcut was found: does a 2-layer model learn SINGLE-QUERY associative recall
when dense auxiliary queries hide their answers? Reports the honest single-query accuracy and the
counterfactual battery at the end. Usage: python probe8.py <tag> <pos_method> [steps]"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from context_lab.data import TaskConfig, make_dataset  # noqa: E402
from context_lab.evaluation import predict  # noqa: E402
from context_lab.interventions.counterfactual import battery_summary, counterfactual_battery  # noqa: E402
from context_lab.models import ModelConfig  # noqa: E402
from context_lab.training import TrainConfig, train_model  # noqa: E402
tag, pm = sys.argv[1], sys.argv[2]
steps = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
tc = TaskConfig(seq_len=(24, 64), n_pairs=(2, 8), n_lures=(0, 1), lure_prob=0.25, n_queries="all",
                single_query_prob=0.25, query_format="ans_marker", aux_show_answers=False)
tr = TrainConfig(steps=steps, lr=3e-3, warmup_steps=100, eval_every=250, log_every=250, threads=2, val_examples=256)
m, h, s = train_model(ModelConfig(pos_method=pm, n_heads=2), tc, tr,
                      log_fn=lambda r: print(tag, r["step"], f"val={r['val_acc']:.3f} t={r['elapsed_s']:.0f}", flush=True))
single = make_dataset(tc.eval_format(), 400, 99, "probe8/single")
print(tag, "SINGLE-QUERY ACC", round(float(predict(m, single)["correct"].mean()), 3), flush=True)
print(tag, "BATTERY", {k: round(v, 3) for k, v in battery_summary(counterfactual_battery(m, single)).items()
                       if v is not None and not k.endswith("_n")}, flush=True)
