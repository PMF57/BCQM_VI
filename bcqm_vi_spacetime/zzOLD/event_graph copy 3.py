from __future__ import annotations

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

    def _adj_undirected(self, active: Set[int]) -> Dict[int, Set[int]]:
        adj: Dict[int, Set[int]] = {e: set() for e in active}
        for u, v, t in self.edges:
            if u in active and v in active:
                adj[u].add(v)
                adj[v].add(u)
        return adj

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
        return sum(coeffs) / len(coeffs) if coeffs else 0.0

    def _largest_component(self, adj: Dict[int, Set[int]]) -> List[int]:
        seen: Set[int] = set()
        best: List[int] = []
        for e in adj.keys():
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
            if len(comp) > len(best):
                best = comp
        return best

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
        Estimate spectral dimension d_s from random-walk return probability on the
        largest connected component of the undirected projection of the active subgraph.

        P(t) ~ t^{-d_s/2}. We fit log P vs log t over [fit_t_min, fit_t_max].
        """
        adj_all = self._adj_undirected(active)
        comp = self._largest_component(adj_all)
        if len(comp) < 10:
            return {"ds_est": None, "reason": "component_too_small", "comp_size": len(comp)}
        comp_set = set(comp)
        adj = {v: [nb for nb in adj_all[v] if nb in comp_set] for v in comp}
        rng = random.Random(int(seed))
        nodes = comp

        # Return probability per t: fraction of walkers back at start
        P = [0.0] * (t_max + 1)
        for _ in range(n_walkers):
            start = rng.choice(nodes)
            pos = start
            for t in range(1, t_max + 1):
                nbrs = adj.get(pos, [])
                if nbrs:
                    pos = rng.choice(nbrs)
                # else isolated; stay
                if pos == start:
                    P[t] += 1.0
        for t in range(1, t_max + 1):
            P[t] /= float(n_walkers)

        # Fit slope on log-log for t in [fit_t_min, fit_t_max]
        xs, ys = [], []
        for t in range(max(1, fit_t_min), min(t_max, fit_t_max) + 1):
            if P[t] > 0:
                xs.append(math.log(t))
                ys.append(math.log(P[t]))
        if len(xs) < 3:
            return {"ds_est": None, "reason": "insufficient_positive_returns", "comp_size": len(comp)}
        xbar = sum(xs) / len(xs)
        ybar = sum(ys) / len(ys)
        num = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
        den = sum((x - xbar) ** 2 for x in xs)
        if den <= 0:
            return {"ds_est": None, "reason": "degenerate_fit", "comp_size": len(comp)}
        slope = num / den
        ds = -2.0 * slope
        return {
            "ds_est": float(ds),
            "fit_t_min": int(fit_t_min),
            "fit_t_max": int(fit_t_max),
            "t_max": int(t_max),
            "n_walkers": int(n_walkers),
            "comp_size": int(len(comp)),
            "P_return_sample": [float(P[t]) for t in range(1, min(t_max, 12) + 1)],
        }
