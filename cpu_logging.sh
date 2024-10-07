log_dir=./data/out/"$(date +%s)"
mkdir -p "$log_dir"
./latency_exp.sh

func_list="$(kubectl get pods | grep func | awk '{print $1}')"
read -r -a lines <<< "$(echo -e "$func_list" | tr '\n' ' ')"

for func in "${lines[@]}"; do
  kubectl top pod "$func" >> "$log_dir"/log_func.log
done
