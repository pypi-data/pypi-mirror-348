# -*- coding: utf-8 -*-
"""
---------------------------------------------
Created on 2025/3/5 21:40
@author: ZhangYundi
@email: yundi.xxii@outlook.com
---------------------------------------------
"""
from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path

import polars as pl
from toolz import partial
from functools import lru_cache

import ygo
import ylog
from .errors import CalculateError, PolarsError
from .expr import Expr
import time

# 动态加载模块
module_name = "udf"
module_path = Path(__file__).parent / "udf" / "__init__.py"
spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = module
spec.loader.exec_module(module)


@dataclass
class FailInfo:
    expr: str
    error: Exception

    def __str__(self):
        return f"""
expr={self.expr}
=================================================
{self.error}
=================================================
"""

    def __repr__(self):
        return self.__str__()

@lru_cache(maxsize=512)
def parse_expr(expr: str) -> Expr:
    return Expr(expr)

class QDF:

    def __init__(self,
                 data: pl.LazyFrame,
                 index: tuple[str] = ("date", "time", "asset"),
                 align: bool = True,):
        self.data = data.with_columns(pl.col(pl.Decimal).cast(pl.Float32))
        self.dims = [self.data.select(index_).drop_nulls().unique().count().collect().item() for index_ in index]
        if align:
            lev_vals: list[pl.DataFrame] = [self.data.select(name).drop_nulls().unique() for name in index]
            full_index = lev_vals[0]
            for lev_val in lev_vals[1:]:
                full_index = full_index.join(lev_val, how="cross")
            self.data = full_index.join(self.data, on=index, how='left') #.sort(index).collect().lazy()

        self.index = index
        self.failed = list()

    def __str__(self):
        return self.data.__str__()

    def __repr__(self):
        return self.data.__str__()

    def register_udf(self, func: callable, name: str = None):
        name = name if name is not None else func.__name__
        setattr(module, name, func)

    def _compile_expr(self, expr: str, cover: bool):
        expr_parsed = Expr(expr)
        alias = expr_parsed.alias  # if expr_parsed.alias is not None else str(expr_parsed)
        current_cols = set(self.data.collect_schema().keys())
        columns = self.data.collect_schema().names()
        if alias in current_cols and not cover:
            return alias

        def calc(expr_: Expr):
            alias_ = expr_.alias
            # _cols = self.data.collect_schema().names()
            if alias_ in current_cols and not cover:
                # 已存在：直接select数据源
                return alias_
            func = getattr(module, expr_.fn_name)
            _params = ygo.fn_signature_params(func)
            if "dims" in _params:
                func = partial(func, dims=self.dims)
            args = list()
            kwargs = dict()
            for arg in expr_.args:
                if isinstance(arg, Expr):
                    args.append(pl.col(calc(arg)))
                elif isinstance(arg, dict):
                    kwargs.update(arg)
                elif isinstance(arg, str):
                    args.append(pl.col(arg))
                else:
                    args.append(arg)  # or args.append(pl.lit(arg))
            try:
                expr_pl: pl.Expr = func(*args, **kwargs).alias(alias_)
            except Exception as e:
                raise CalculateError(f"{expr_.fn_name}({', '.join([str(arg) for arg in args])})\n{e}")
            try:
                self.data = self.data.with_columns(expr_pl)
            except Exception as e:
                raise PolarsError(f"{expr_}\n{e}")
            return alias_

        calc(expr_parsed)

        columns.append(alias)
        drop = current_cols.difference(set(columns))
        self.data = self.data.drop(*drop)

        return alias

    def sql(self, *exprs: str, cover: bool = False,) -> pl.LazyFrame:
        """
        表达式查询
        Parameters
        ----------
        exprs: str
            表达式，比如 "ts_mean(close, 5) as close_ma5"
        cover: bool
            当遇到已经存在列名的时候，是否重新计算覆盖原来的列, 默认False，返回已经存在的列，跳过计算
            - True: 重新计算并且返回新的结果，覆盖掉原来的列
            - False, 返回已经存在的列，跳过计算
        Returns
        -------
            polars.DataFrame
        """
        self.failed = list()
        exprs_to_add = list()
        for expr in exprs:
            try:
                compiled = self._compile_expr(expr, cover)
                if compiled is not None:
                    exprs_to_add.append(compiled)
            except Exception as e:
                self.failed.append(FailInfo(expr, e))
        if self.failed:
            ylog.warning(f"QDF.sql 失败：{len(self.failed)}/{len(exprs)}: \n {self.failed}")
        final_df = self.data.with_columns(exprs_to_add).select(*self.index, *exprs_to_add).fill_nan(None).drop_nulls().sort(self.index)
        return final_df.collect()

