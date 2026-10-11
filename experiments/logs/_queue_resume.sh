#!/usr/bin/env bash
# one-off: resume the study queue after the manual pause (waits for the induction extension)
until grep -q "^done:" experiments/logs/study_induction.log 2>/dev/null; do sleep 20; done
echo "=== $(date '+%F %T') queue resumed (induction extension finished)" >> experiments/logs/run_all.log
for study in main_pe multihop train_length similarity; do
  echo "=== $(date '+%F %T') start $study" >> experiments/logs/run_all.log
  python ctxlab.py study "configs/study_${study}.yaml" --workers 3 --threads 2 >> "experiments/logs/study_${study}.log" 2>&1
  echo "=== $(date '+%F %T') end $study (exit $?)" >> experiments/logs/run_all.log
done
python ctxlab.py dynamics main_pe >> experiments/logs/dynamics_main_pe.log 2>&1
python ctxlab.py dynamics multihop >> experiments/logs/dynamics_multihop.log 2>&1
echo "=== $(date '+%F %T') all studies finished" >> experiments/logs/run_all.log
