#!/usr/bin/env bash
# one-off: after the density study, run the shortcut dose-response study and its learning dynamics
until grep -q "^done:" experiments/logs/study_density.log 2>/dev/null; do sleep 20; done
echo "=== $(date '+%F %T') start shortcut_dose" >> experiments/logs/run_all.log
python ctxlab.py study configs/study_shortcut_dose.yaml --workers 3 --threads 2 >> experiments/logs/study_shortcut_dose.log 2>&1
echo "=== $(date '+%F %T') end shortcut_dose (exit $?)" >> experiments/logs/run_all.log
python ctxlab.py dynamics shortcut_dose >> experiments/logs/dynamics_shortcut_dose.log 2>&1
echo "=== $(date '+%F %T') dynamics shortcut_dose finished" >> experiments/logs/run_all.log
