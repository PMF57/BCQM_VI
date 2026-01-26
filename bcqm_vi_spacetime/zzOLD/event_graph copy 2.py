from __future__ import annotations

"""
event_graph.py (BCQM VI Path A + geometry)

Minimal event graph bookkeeping + spatial observables + spectral dimension probe.

Spectral dimension estimate:
- run many random walks on the largest undirected connected component of V_active
- measure return probability P0(t)
- fit slope of log P0(t) vs log t over a fit range
- ds ≈ -2 * slope
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple
import math
import random


@dataclass
class EventNode:
    created_at: int
    domain: Optional[int] = None
    indeg: int = 0
    outdeg: int = 0


class EventGraph:
    def __init__(self) -> None:
        self.nodes: Dict[int, EventNode] = {}
        self.edges: List[Tuple[int, int, int]] = []  # (u,v,t)
        self._next_id: int = 0

    def new_event(self, t: int, domain: Optional[int] = None) -> int:
        eid = self._next_id
        self._next_id += 1
        self.nodes[eid] = EventNode(created_at=int(t), domain=domain, indeg=0, outdeg=0)
        return eid

    def add_edge(self, u: int, v: int, t: int) -> None:
        self.edges.append((int(u), int(v), int(t)))
        self.nodes[u].outdeg += 1
        self.nodes[v].indeg += 1

    def v_active(self, t: int, W_coh: int, frontiers: List[int]) -> Set[int]:
        cutoff = int(t) - int(W_coh)
        active = {eid for eid, nd in self.nodes.items() if nd.created_at >= cutoff}
        active.update(int(e) for e in frontiers)
        return active

    def _adj_undirected(self, active: Set[int]) -> Dict[int, Set[int]]:
        adj: Dict[int, Set[int]] = {e: set() for e in active}
        for u, v, tt in self.edges:
            if u in active and v in active:
                adj[u].add(v)
                adj[v].add(u)
        return adj

    def indegrees(self, active: Set[int]) -> List[int]:
        return [self.nodes[e].indeg for e in active]

    def max_indegree(self, active: Set[int]) -> int:
        return max((self.nodes[e].indeg for e in active), default=0)

    def hubshare(self, active: Set[int]) -> float:
        indegs = self.indegrees(active)
        if not indegs:
            return 0.0
        s = sum(indegs)
        return (max(indegs) / float(s)) if s > 0 else 0.0

    def s_junc_w(self, active: Set[int], beta: float = 1.5) -> float:
        if not active:
            return 0.0
        s = 0.0
        for e in active:
            k = self.nodes[e].indeg
            if k < 2:
                continue
            if k == 2:
                s += 1.0
            else:
                s += float(k) ** float(beta)
        return s / float(len(active))

    def s_perc(self, active: Set[int]) -> float:
        if not active:
            return 0.0
        adj = self._adj_undirected(active)
        seen: Set[int] = set()
        best = 0
        for e in active:
            if e in seen:
                continue
            stack = [e]
            seen.add(e)
            size = 0
            while stack:
                x = stack.pop()
                size += 1
                for nb in adj.get(x, set()):
                    if nb not in seen:
                        seen.add(nb)
                        stack.append(nb)
            best = max(best, size)
        return best / float(len(active))

    def clustering_coeff(self, active: Set[int], sample: Optional[int] = 500) -> float:
        if not active:
            return 0.0
        adj = self._adj_undirected(active)
        nodes = list(active)
        if sample is not None and len(nodes) > sample:
            step = max(1, len(nodes) // sample)
            nodes = nodes[::step][:sample]
        coeffs: List[float] = []
        for v in nodes:
            nbrs = list(adj.get(v, set()))
            k = len(nbrs)
            if k < 2:
                continue
            links = 0
            for i in range(k):
                ai = adj.get(nbrs[i], set())
                for j in range(i + 1, k):
                    if nbrs[j] in ai:
                        links += 1
            coeffs.append((2.0 * links) / (k * (k - 1)))
        return (sum(coeffs) / len(coeffs)) if coeffs else 0.0

    def _largest_component(self, active: Set[int]) -> List[int]:
        adj = self._adj_undirected(active)
        seen: Set[int] = set()
        best_comp: List[int] = []
        for e in active:
            if e in seen:
                continue
            stack = [e]
            seen.add(e)
            comp: List[int] = []
            while stack:
                x = stack.pop()
                comp.append(x)
                for nb in adj.get(x, set()):
                    if nb not in seen:
                        seen.add(nb)
                        stack.append(nb)
            if len(comp) > len(best_comp):
                best_comp = comp
        return best_comp

    def estimate_spectral_dimension(
        self,
        active: Set[int],
        *,
        t_max: int = 60,
        n_walkers: int = 300,
        fit_t_min: int = 5,
        fit_t_max: int = 30,
        seed: int = 0,
    ) -> Dict[str, object]:
        """
        Estimate spectral dimension ds on the largest undirected component within V_active.

        Returns dict with ds_est, slope, fit range, return_probs.
        """
        comp = self._largest_component(active)
        if len(comp) < 10:
            return {"ds_est": None, "reason": "component_too_small", "comp_size": len(comp)}

        adj_sets = self._adj_undirected(set(comp))
        # precompute neighbour lists (must be non-empty for connected component)
        nbrs: Dict[int, List[int]] = {v: list(adj_sets[v]) for v in comp if adj_sets.get(v)}
        if not nbrs:
            return {"ds_est": None, "reason": "no_neighbours", "comp_size": len(comp)}

        rng = random.Random(int(seed))
        starts = [rng.choice(comp) for _ in range(int(n_walkers))]
        # simulate each walker once
        returns = [0] * (t_max + 1)  # returns[t] count
        for s in starts:
            pos = s
            for t in range(1, t_max + 1):
                nn = nbrs.get(pos)
                if not nn:
                    break
                pos = rng.choice(nn)
                if pos == s:
                    returns[t] += 1

        P0 = []
        t_vals = []
        for t in range(1, t_max + 1):
            p = returns[t] / float(n_walkers)
            P0.append(p)
            t_vals.append(t)

        # Fit on [fit_t_min, fit_t_max] where P0>0
        xs = []
        ys = []
        for t, p in zip(t_vals, P0):
            if t < fit_t_min or t > fit_t_max:
                continue
            if p <= 0:
                continue
            xs.append(math.log(t))
            ys.append(math.log(p))
        if len(xs) < 3:
            return {"ds_est": None, "reason": "insufficient_fit_points", "comp_size": len(comp), "return_probs": P0}

        # Linear regression slope
        xbar = sum(xs) / len(xs)
        ybar = sum(ys) / len(ys)
        num = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
        den = sum((x - xbar) ** 2 for x in xs)
        slope = num / den if den > 0 else 0.0
        ds = -2.0 * slope

        return {
            "ds_est": ds,
            "slope": slope,
            "fit_t_min": fit_t_min,
            "fit_t_max": fit_t_max,
            "t_max": t_max,
            "n_walkers": n_walkers,
            "comp_size": len(comp),
            "comp_fraction": len(comp) / float(len(active)) if active else 0.0,
            "return_probs": P0,
        }
