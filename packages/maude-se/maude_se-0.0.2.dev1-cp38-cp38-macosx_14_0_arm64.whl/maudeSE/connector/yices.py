import time

from yices import *
from maudeSE.maude import *
from maudeSE.util import id_gen
from maudeSE.maude import *

class YicesConnector(Connector):
    def __init__(self, converter: Converter, logic=None):
        super().__init__()
        self._c = converter
        self._g = id_gen()

        _logic = "QF_LRA" if logic is None else logic

        # time
        self._tt = 0.0
        self._dt = 0.0
        self._st = 0.0
        self._mt = 0.0

        # set solver
        self._cfg: Config = Config()
        self._cfg.default_config_for_logic(_logic)

        self._ctx: Context = Context(self._cfg)
        self._m = None
    
    def check_sat(self, consts):
        fs = list()
        for const in consts:
            (c, _), _, _ = const.data()
            fs.append(c)

        self._ctx.assert_formulas(fs)
        r = self._ctx.check_context()

        if r == Status.SAT:
            return True
        elif r == Status.UNSAT:
            return False
        else:
            raise Exception("failed to handle check sat (solver give-up)")
        
    def push(self):
        self._ctx.push()

    def pop(self):
        self._ctx.pop()
    
    def reset(self):
        self._ctx.reset_context()

    def add_const(self, acc, cur):
        # initial case
        if acc is None:
            ((cur_t, _), _, cur_v) = cur.data()
            body = cur_t

        else:
            ((acc_f, _), _, acc_v), ((cur_t, _), _, cur_v) = acc.data(), cur.data()
            body = Terms.yand([acc_f, cur_t])

        return SmtTerm([(body, Terms.type_of_term(body)), None, None])

    def subsume(self, subst, prev, acc, cur):
        s = time.time()

        d_s = time.time()
        t_v, t_l = list(), list()
        sub = subst.keys()
        for p in sub:
            (src, _), _, _ = self._c.dag2term(p).data()
            (trg, _), _, _ = self._c.dag2term(subst.get(p)).data()

            t_v.append(src)
            t_l.append(trg)

        d_e = time.time()

        self._dt += d_e - d_s

        (prev_c, _), _, _ = prev.data()

        (acc_c, _), _, _ = acc.data()
        (cur_c, _), _, _ = cur.data()
    
        so_s = time.time()
        self._ctx.push()
        self._ctx.assert_formula(Terms.ynot(Terms.implies(Terms.yand([acc_c, cur_c]), Terms.subst(t_v, t_l, prev_c))))

        r = self._ctx.check_context()

        self._ctx.pop()
        so_e = time.time()
        self._st += so_e - so_s

        if r == Status.UNSAT:
            e = time.time()
            self._tt += e - s
            return True
        elif r == Status.SAT:
            e = time.time()
            self._tt += e - s
            return False
        else:
            raise Exception("failed to apply subsumption (give-up)")

    def merge(self, subst, prev_t, prev, cur_t, acc, cur):
        pass

    def get_model(self):
        raw_m = Model.from_context(self._ctx, 1)
        m = SmtModel()
        for t in raw_m.collect_defined_terms():
            try:
                ty = Terms.type_of_term(t)
                k, v = [(t, ty), None, None], [(Terms.parse_term(str(raw_m.get_value(t)).lower()), ty), None, None]
                m.set(k, v)
            except:
                continue
        return m
    
    def print_model(self):
        print(self._m.to_string(80, 100, 0))

    def set_logic(self, logic):
        self._ctx.dispose()

        self._cfg: Config = Config()
        self._cfg.default_config_for_logic(logic)

        self._ctx: Context = Context(self._cfg)
        self._m = None

    def get_converter(self):
        return self._c




















# class YicesConverter(Converter):
#     """A term converter from Maude to Yices"""

#     def __init__(self):
#         self._cfg: Config = Config()
#         self._cfg.default_config_for_logic("QF_LRA")

#         self._ctx: Context = Context(self._cfg)
#         self._model = None

#     def __del__(self):
#         self._ctx.dispose()
#         self._cfg.dispose()

#     def make_assignment(self):
#         if self._model is None:
#             raise Exception("Yices solver error occurred during making assignment (no model exists)")
#         return YicesAssignment(self._model)

#     def push(self):
#         self._ctx.push()

#     def pop(self):
#         self._ctx.pop()

#     def reset(self):
#         self._ctx.reset_context()

#     def add(self, formula: Formula):
#         self._ctx.assert_formula(Terms.parse_term(translate(formula)))

#     def assert_and_track(self, formula: Formula, track_id: str):
#         pass

#     def unsat_core(self):
#         return self._ctx.get_unsat_core()

#     def _clear_model(self):
#         if self._model is not None:
#             self._model.dispose()
#             self._model = None



# class YicesAssignment(Assignment):
#     def __init__(self, _yices_model):
#         self._yices_model = _yices_model
#         Assignment.__init__(self)

#     # solver_model_to_generalized_model
#     def _get_assignments(self):
#         new_dict = dict()
#         for e in self._yices_model.collect_defined_terms():
#             t, v = Terms.to_string(e), self._yices_model.get_float_value(e)
#             if Terms.is_real(e):
#                 new_dict[Real(t)] = RealVal(str(v))
#             elif Terms.is_int(e):
#                 new_dict[Int(t)] = IntVal(str(v))
#             elif Terms.is_bool(e):
#                 new_dict[Bool(t)] = BoolVal(str(v))
#             else:
#                 Exception("cannot generate assignments")
#         return new_dict
