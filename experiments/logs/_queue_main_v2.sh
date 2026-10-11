#!/usr/bin/env bash
# one-off: after the shortcut dose study, run the main study v2, its learning dynamics and mechanistic analysis
until grep -q "dynamics shortcut_dose finished" experiments/logs/run_all.log 2>/dev/null; do sleep 30; done
echo "=== $(date '+%F %T') start main_pe (v2)" >> experiments/logs/run_all.log
python ctxlab.py study configs/study_main_pe.yaml --workers 3 --threads 2 >> experiments/logs/study_main_pe_v2.log 2>&1
echo "=== $(date '+%F %T') end main_pe v2 (exit $?)" >> experiments/logs/run_all.log
python ctxlab.py dynamics main_pe >> experiments/logs/dynamics_main_pe.log 2>&1
python ctxlab.py analyze main_pe --seeds 0 --n 200 --n-patch 24 >> experiments/logs/analyze_main_pe.log 2>&1
python ctxlab.py interp main_pe >> experiments/logs/interp_main_pe.log 2>&1
echo "=== $(date '+%F %T') main_pe v2 dynamics+analysis+interp finished" >> experiments/logs/run_all.log
