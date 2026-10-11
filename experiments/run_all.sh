#!/usr/bin/env bash
# Run every study sequentially (each study parallelises its own runs).
# Cached runs (same configuration hash) are skipped, so this script is safe to re-run.
# Usage (from the project root):  bash experiments/run_all.sh [workers] [threads]
set -u
WORKERS=${1:-3}
THREADS=${2:-2}
mkdir -p experiments/logs
for study in fillers induction main_pe multihop train_length similarity shortcut_dose; do
  echo "=== $(date '+%F %T') start $study" | tee -a experiments/logs/run_all.log
  python ctxlab.py study "configs/study_${study}.yaml" --workers "$WORKERS" --threads "$THREADS" \
    >> "experiments/logs/study_${study}.log" 2>&1
  echo "=== $(date '+%F %T') end $study (exit $?)" | tee -a experiments/logs/run_all.log
done
python ctxlab.py dynamics main_pe >> experiments/logs/dynamics_main_pe.log 2>&1
python ctxlab.py dynamics multihop >> experiments/logs/dynamics_multihop.log 2>&1
python ctxlab.py dynamics shortcut_dose >> experiments/logs/dynamics_shortcut_dose.log 2>&1
echo "=== $(date '+%F %T') all studies finished" | tee -a experiments/logs/run_all.log
