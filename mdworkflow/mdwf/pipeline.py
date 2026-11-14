"""③~⑥ 한 번에: 셀 → 실행 → 물성 → 결과 표. 폐루프(loop/)가 후보 하나마다 부른다."""
import argparse
from .common import workspace
from . import builder, runner, analyze, store


def one(cid, ws, sara=None, comp=None, atoms=3000, T=298.0, protocol="standard", seed=1, threads=4, source=""):
    if sara:
        c, act = builder.sara_to_counts(sara, ws, atoms); info = {"target_wt": list(sara), "actual_wt": act}
    else:
        c, info = comp, None
    builder.build(cid, c, ws, seed=seed, sara_info=info)
    s = runner.execute(cid, ws, T=T, protocol=protocol, seed=4928459 + seed, threads=threads)
    if not s["ok"]:
        return store.store(cid, ws, source)
    analyze.analyze(cid, ws)
    return store.store(cid, ws, source)


def main(argv=None):
    ap = argparse.ArgumentParser(description="셀 → 실행 → 물성 → 기록 (MD 워크플로우 ③~⑥)")
    ap.add_argument("--id", required=True); ap.add_argument("--sara"); ap.add_argument("--comp"); ap.add_argument("--atoms", type=int, default=3000)
    ap.add_argument("--T", type=float, default=298.0); ap.add_argument("--protocol", default="standard"); ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--threads", type=int, default=4); ap.add_argument("--source", default=""); ap.add_argument("--ws")
    a = ap.parse_args(argv); ws = workspace(a.ws)
    r = one(a.id, ws, [float(x) for x in a.sara.split(",")] if a.sara else None, builder.parse_comp(a.comp) if a.comp else None,
            a.atoms, a.T, a.protocol, a.seed, a.threads, a.source)
    print(f"완료 {a.id}: ρ {r['density_gcm3']} ± {r['density_se']} · CED {r['ced_MJm3']} ± {r['ced_se']} · ok {r['ok']} · {r['wall_s']} s")


if __name__ == "__main__":
    main()
