"""Verify feasibility, raw objectives, reference bounds, histories and summaries."""
from pathlib import Path
import argparse,itertools,json,statistics,math,hashlib
import numpy as np
from coverage import arrays,value,greedy
from search import run,PARAMS
ROOT=Path(__file__).resolve().parent
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rerun',action='store_true');ap.add_argument('--results',type=Path,default=ROOT/'results');args=ap.parse_args()
    data=json.loads((args.results/'experiment.json').read_text())
    cases={c['id']:c for c in data['cases']}
    for name,digest in data['metadata']['source_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
    for case in cases.values():
        matrix,weights=arrays(case)
        coords=np.asarray(case['facilities']);demand=np.asarray(case['demand'])
        np.testing.assert_array_equal(matrix,np.linalg.norm(coords[:,None]-demand[None,:],axis=2)<=case['radius'])
        assert case['baseline']==value(case['baseline_selection'],matrix,weights)
        ref=case['reference']
        if ref['kind']=='exact':
            # Independently sum the union instead of using the search objective.
            answer=max(sum(weights[j] for j in range(len(weights)) if any(matrix[i,j] for i in s)) for s in itertools.combinations(range(len(matrix)),case['k']))
            assert answer==ref['value']
        else:
            upper=min(sum(weights[j] for j in range(len(weights)) if any(matrix[:,j])),sum(sorted(sum(weights[j] for j in range(len(weights)) if matrix[i,j]) for i in range(len(matrix)))[-case['k']:]))
            assert ref['value']==upper
    for row in data['runs']:
        case=cases[row['case']]
        chosen=row['selected'];matrix,weights=arrays(case)
        assert len(chosen)==len(set(chosen))==case['k']
        assert all(0<=i<len(matrix) for i in chosen)
        actual=sum(int(weights[j]) for j in range(len(weights)) if any(matrix[i,j] for i in chosen))
        assert actual==row['objective']
        assert case['baseline']<=actual<=case['reference']['value']
        assert row['evaluations']==PARAMS['population']*(PARAMS['iterations']+1)
        assert len(row['history'])==PARAMS['iterations']+1
        assert row['history'][-1]==row['objective']
        assert all(b>=a for a,b in zip(row['history'],row['history'][1:]))
        ref=case['reference']['value'];objective=row['objective']
        assert math.isclose(row['gap_pct'],100*(ref-objective)/ref,abs_tol=1e-10)
        assert row['seconds']>=0
        if args.rerun and row['trial']==0:
            fresh=run(case,row['algorithm'],row['seed'])
            for key in ['selected','objective','history','evaluations']:assert fresh[key]==row[key],(row['case'],row['algorithm'],key)
    for summary in data['summary']:
        rows=[x for x in data['runs'] if x['size']==summary['size'] and x['algorithm']==summary['algorithm']]
        ids=sorted({x['case'] for x in rows})
        expected={'runs':len(rows),'mean_objective':statistics.mean(x['objective'] for x in rows),
                  'best_objective':max(x['objective'] for x in rows),
                  'mean_gap_pct':statistics.mean(x['gap_pct'] for x in rows),
                  'mean_seconds':statistics.mean(x['seconds'] for x in rows),
                  'mean_within_case_sd':statistics.mean(statistics.stdev(x['objective'] for x in rows if x['case']==cid) for cid in ids)}
        for key,val in expected.items():assert math.isclose(summary[key],val,abs_tol=1e-10)
    print('PASS:',len(cases),'cases,',len(data['runs']),'runs; constraints, bounds, traces and summaries verified'+('; first runs reproduced' if args.rerun else ''))
if __name__=='__main__':main()
