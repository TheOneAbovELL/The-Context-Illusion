#!/usr/bin/env bash
# one-off: wait for the already-running fillers study, then run the rest of the queue
until grep -q "^done:" experiments/logs/study_fillers.log 2>/dev/null; do sleep 20; done
echo "=== $(date '+%F %T') fillers finished (started manually)" >> experiments/logs/run_all.log
for study in induction main_pe multihop train_length similarity; do
  echo "=== $(date '+%F %T') start $study" >> experiments/logs/run_all.log
  python ctxlab.py study "configs/study_${study}.yaml" --workers 3 --threads 2 >> "experiments/logs/study_${study}.log" 2>&1
  echo "=== $(date '+%F %T') end $study (exit $?)" >> experiments/logs/run_all.log
done
python ctxlab.py dynamics main_pe >> experiments/logs/dynamics_main_pe.log 2>&1
python ctxlab.py dynamics multihop >> experiments/logs/dynamics_multihop.log 2>&1
echo "=== $(date '+%F %T') all studies finished" >> experiments/logs/run_all.log
