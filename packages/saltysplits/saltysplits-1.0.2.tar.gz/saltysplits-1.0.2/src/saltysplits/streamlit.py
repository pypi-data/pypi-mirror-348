import numpy as np
import re
import pandas as pd
from pathlib import Path
import streamlit as st
import saltysplits as ss
import altair as alt
from typing import List
from saltysplits.annotations import encode_time
from saltysplits import SaltySplits
from saltysplits import DEMO_SPLITS
from saltysplits import TimeType


st.set_page_config(
    page_title="Sup! - SaltySplits.com",
    page_icon="🧂",
    initial_sidebar_state="expanded",
    layout="wide",
    menu_items={
        'Get help': 'https://github.com/jaspersiebring/saltysplits',
        'Report a bug': "https://github.com/jaspersiebring/saltysplits/issues/new",
    }
)

@st.cache_data
def represent_resets(splits_df: pd.DataFrame) -> pd.DataFrame:
    reset_indices = np.argmax(splits_df.isna(), axis=0)
    reset_segments = np.array(splits_df.index)[reset_indices]
    reset_segment_names, reset_segment_counts = np.unique(reset_segments, return_counts=True)
    reset_df = pd.DataFrame({"Segment": reset_segment_names, "Count": reset_segment_counts})
    return reset_df

@st.cache_data
def represent_time(td_series: pd.Series, include_ns: bool = False) -> pd.DataFrame:
    dt_series = pd.to_datetime(td_series, unit="ns")  
    ht_series = td_series.apply(lambda x: encode_time(x, include_ns=include_ns) if pd.notna(x) else None) 
    time_dataframe = pd.concat([ht_series, dt_series], axis=1) 
    time_dataframe.columns = ["Time", "DateTime"]
    time_dataframe = time_dataframe.rename_axis("id").reset_index()
    return time_dataframe

@st.cache_data
def demo_splits(lss_path: Path = DEMO_SPLITS) -> SaltySplits:
    splits = ss.read_lss(lss_path=lss_path)
    return splits

@st.cache_data
def splits_from_bytes(lss_bytes: bytes) -> SaltySplits:
    return SaltySplits.from_xml(lss_bytes)

@st.cache_data
def splits_dataframe(splits_bytes: bytes, time_type: TimeType, allow_partial: bool, allow_empty: bool = False, cumulative: bool = False, lss_repr: bool = False, lss_ns: bool = True) -> pd.DataFrame:
    # mainly exists because we can't cache SaltySplits instances (add kwargs though)
    splits = splits_from_bytes(splits_bytes)
    dataframe = splits.to_df(
        time_type=time_type,
        allow_partial=allow_partial,
        allow_empty=allow_empty,
        cumulative=cumulative,
        lss_repr=lss_repr, 
        lss_ns=lss_ns
    )
    return dataframe
    
@st.cache_data
def read_bytes(path: Path) -> bytes:
    with open(path, "rb") as file:
        return file.read()


@st.cache_data
def splits_metrics(splits_bytes: bytes, time_type: TimeType) -> None:
    splits = splits_from_bytes(splits_bytes)
    splits_df = splits_dataframe(splits_bytes, time_type=time_type, allow_partial=True)

    complete_runs = splits_df.loc[:, ~splits_df.isna().any()]  
    run_times = complete_runs.sum(axis=0)
    best_run_index = run_times.argmin()
    best_run = run_times.iloc[best_run_index]
    best_run = encode_time(best_run, include_ns=False)

    best_segments = splits_df.min(axis=1)
    best_segments_sum = best_segments.sum()
    best_segments_sum = encode_time(best_segments_sum, include_ns=False)
    life_playtime = splits_df.sum(axis=0).sum()
    life_playtime = encode_time(life_playtime, include_ns=False)
    best_diffs = complete_runs.iloc[:, best_run_index] - best_segments
    possible_timesave = best_diffs.sum()
    possible_timesave = encode_time(possible_timesave, include_ns=False)

    time_column, segment_column, timesave_column, attempts_column, playtime_column = st.columns(5)
    time_column.metric("BEST TIME", best_run)
    segment_column.metric("SUM OF BEST SEGMENTS", best_segments_sum)
    timesave_column.metric("POSSIBLE TIMESAVE", possible_timesave)
    attempts_column.metric("ATTEMPTS", f"{splits.attempt_count}")
    playtime_column.metric("LIFE PLAYTIME", life_playtime)

@st.cache_data
def rank_splits(dataframe, n: int = 3) -> List[str]:
    # LEGACY (add_suffix)
    ranked_indices = []
    for name, group in dataframe.T.groupby(lambda x: re.findall(r'\((.*)\)', x)[0]):
        complete_group = group.T.loc[:, ~group.T.isna().any()] 
        ranked_indices.extend(complete_group.sum(axis=0).sort_values().head(n).index.tolist())
    return ranked_indices


def resets_piechart(
    dataframe: pd.DataFrame,
    title: str = "Resets Per Segment",
) -> None:

    highlight = alt.selection_point(
        fields=["Segment"],
        on="mouseover",
        clear="mouseout",
        empty="all",
        bind="legend"
    )

    chart = alt.Chart(
        dataframe,
        title=alt.Title(title, anchor="middle")
    ).mark_arc(
        innerRadius=50,
        cursor="pointer",
        stroke="white",
        strokeWidth=2
    ).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(
            field="Segment",
            type="nominal",
            legend=alt.Legend(
                symbolSize=200,
                symbolStrokeColor=None,
                symbolStrokeWidth=0
            )
        ),
        opacity=alt.condition(highlight, alt.value(1), alt.value(0.3))
    ).add_params(highlight)

    st.altair_chart(chart)


def time_linegraph(
    dataframe: pd.DataFrame,
    title: str,
    x_title: str,
    y_title: str,
    interpolation_method: str = "monotone",
) -> None:

    nearest = alt.selection_point(
        nearest=True, on="pointerover", fields=["id"], empty=False, clear="pointerout"
    )

    line_graph = alt.Chart(
        dataframe,
        title=alt.Title(title, anchor="middle")
    ).mark_line(
        interpolate=interpolation_method,
        orient="horizontal",
        point=True
    ).encode(
        x=alt.X("id:Q", axis=alt.Axis(grid=False, title=x_title)),
        y=alt.Y("DateTime:T", axis=alt.Axis(format="%H:%M:%S", grid=True, title=y_title)),
        order=alt.Order(field="id:Q"),
        tooltip=["id", "Time"],
    )

    points = line_graph.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    rules = alt.Chart(dataframe).mark_rule(color="gray").encode(
        x="id:Q",
        opacity=alt.condition(nearest, alt.value(0.3), alt.value(0)),
        tooltip=["id", "Time"]
    ).add_params(nearest)

    layer = alt.layer(line_graph, points, rules)
    st.altair_chart(layer)


if __name__ == "__main__":
    with st.sidebar:
        LOGO_URL = "https://github.com/user-attachments/assets/5863a3ed-0552-449f-8942-4378fbd1a59e"
        st.markdown(
            f"""
            <div style='display: flex; align-items: center;'>
                <img src='{LOGO_URL}' style='width: 200px; height: 200px;'>
            </div>
            """,
            unsafe_allow_html=True,
        )

        lss_file = st.file_uploader(
            "Upload LSS file",
            type=["lss", "xml"],
            accept_multiple_files=False,
            label_visibility="hidden"
        )
        if lss_file is not None:
            lss_bytes = lss_file.getvalue()
            st.toast("Did you know that you can export your Run Stats? Hover the table and click 'Download as CSV'")
        else:
            lss_bytes = read_bytes(DEMO_SPLITS)

        splits = splits_from_bytes(lss_bytes)
        if "time_type" not in st.session_state:
            st.session_state["time_type"] = TimeType.REAL_TIME

    # LIFETIME STATS
    st.title(f"{splits.game_name} / :primary[{splits.category_name}]")
    splits_metrics(splits_bytes=lss_bytes, time_type=TimeType.REAL_TIME)

    for i, tab in enumerate(st.tabs(["Real Time", "Game Time"])):
        time_type = TimeType(i)
        st.session_state["time_type"] = time_type
        
        with tab:
            with st.container(border=True):
                lifetime_line, resets_pie = st.columns(2, gap="large")
                
                with lifetime_line:
                    # CONSIDER BUNDLING DATA LOADING IN TIME_LINEGRAPH
                    complete_runs = splits_dataframe(lss_bytes, time_type=st.session_state["time_type"], allow_partial=False)
                    run_times = complete_runs.sum(axis=0)
                    run_times_df = represent_time(run_times, include_ns=False)
                    time_linegraph(run_times_df, title="Completed Run Duration over Time", x_title="Attempt Number", y_title = "Run Duration")

                with resets_pie:
                    partial_runs = splits_dataframe(lss_bytes, time_type=st.session_state["time_type"], allow_partial=True)
                    resets_df = represent_resets(partial_runs)
                    resets_piechart(resets_df)
                    
            st.subheader("Run Stats", divider="blue")
            with st.container(border=True):
                n = 2
                complete_runs = splits_dataframe(lss_bytes, time_type=st.session_state["time_type"], allow_partial=False)
                partial_runs = splits_dataframe(lss_bytes, time_type=st.session_state["time_type"], allow_partial=True)

                segment_order = complete_runs.index.to_list()
                default_ids = complete_runs.sum(axis=0).sort_values().head(n).index.to_list()
                run_ids = st.multiselect(f"Select run (includes top {n} runs by default)", options= partial_runs.columns.to_list(), key=f"multirun_selector_{st.session_state["time_type"]}", default=default_ids)
            
                run_table, run_graph = st.columns(2, gap="large")
                with run_table.container():
                    if f"pills_{st.session_state["time_type"]}" not in st.session_state:
                        st.session_state[f"pills_{st.session_state["time_type"]}"] = []

                    format_options = st.session_state[f"pills_{st.session_state["time_type"]}"] 
                    cumulative = "Cumulative" in format_options
                    lss_ns = "Nanoseconds" in format_options

                    table_runs = splits_dataframe(lss_bytes, time_type=st.session_state["time_type"], allow_partial=True, cumulative=cumulative, lss_ns=lss_ns, lss_repr=True)
                    selected_table_runs = table_runs.loc[:, run_ids]
                    st.dataframe(selected_table_runs, height=len(segment_order) * 30, key=f"table_{st.session_state["time_type"]}")
                    format_options = st.pills("Format options", options = ["Cumulative", "Nanoseconds"], key=f"pills_{st.session_state["time_type"]}", selection_mode = "multi", default=[])
                    
                with run_graph:
                    line_runs = splits_dataframe(lss_bytes, time_type=st.session_state["time_type"], allow_partial=True, cumulative=True)
                    selected_line_runs = line_runs.loc[:, run_ids]
                    selected_line_runs = pd.melt(selected_line_runs.T.rename_axis("id").reset_index(), id_vars='id', value_name="TimeDelta", var_name="Segment")
                    selected_line_runs["Time"] = selected_line_runs["TimeDelta"].apply(lambda x: encode_time(x, include_ns=lss_ns) if pd.notna(x) else None) 
                    selected_line_runs["DateTime"] = pd.to_datetime(selected_line_runs["TimeDelta"], unit="ns")

                    line_graph = alt.Chart(selected_line_runs, title=alt.Title("Run Breakdown (Cumulative)", anchor="middle")).mark_line(
                        point=True,
                        interpolate="monotone",
                        orient="horizontal").encode(
                            alt.Y("Segment:N", axis=alt.Axis(grid=True)).title("Segment Name").sort(segment_order),
                            alt.X("DateTime:T", axis=alt.Axis(grid=False, format="%H:%M:%S")).title("Run Duration"),
                            alt.Order(field="DateTime"),
                            color='id:N',
                            tooltip=["Time", "Segment", "id"]
                        ).properties(
                            height=len(segment_order) * 30
                        )
                    st.altair_chart(line_graph)

                st.divider()

                bar_runs = splits_dataframe(lss_bytes, time_type=st.session_state["time_type"], allow_partial=True, cumulative=False)
                selected_bar_runs = bar_runs.loc[:, run_ids]
                selected_bar_runs = pd.melt(selected_bar_runs.T.rename_axis("id").reset_index(), id_vars='id', value_name="TimeDelta", var_name="Segment")
                selected_bar_runs["Time"] = selected_bar_runs["TimeDelta"].apply(lambda x: encode_time(x, include_ns=lss_ns) if pd.notna(x) else None) 
                selected_bar_runs["DateTime"] = pd.to_datetime(selected_bar_runs["TimeDelta"], unit="ns")
                selected_bar_runs["Zero"] = pd.to_datetime(0, unit="ns")

                bar_graph = alt.Chart(selected_bar_runs, title = alt.Title("Run Breakdown (Segmented)", anchor="middle")).mark_bar().encode(
                    alt.Y("DateTime:T", axis=alt.Axis(grid=True, format="%H:%M:%S")).title("Segment Duration"),
                    alt.X("Segment:N", axis=alt.Axis(labelAngle=-90)).title("Segment Name").sort(segment_order),
                    y2="Zero:T",
                    xOffset="id:N",
                    color="id:N"
                )
                st.altair_chart(bar_graph)

            st.subheader("Segment Stats", divider="blue")
            
            segment_runs = splits_dataframe(lss_bytes, time_type=st.session_state["time_type"], allow_partial=True)
            segment_name = st.selectbox("Select segment (defaults to first)", list(segment_runs.index), 0, key=f"segment_selector_{st.session_state["time_type"]}")
            segment_times = segment_runs.loc[segment_name, :]
            segment_times = segment_times.loc[~segment_times.isna()]
            
            with st.container(border=False):
                with st.container(border=True):
                    segment_stats = represent_time(segment_times, include_ns=False)
                    time_linegraph(dataframe=segment_stats, title=f"Segment Duration over Time ({segment_name})", x_title = "Attempt Number", y_title="Segment Duration")

                with st.container(border=True):
                    min_segment, max_segment, mean_segment, median_segment, std_segment = st.columns(5)
                    min_segment.metric(f"MIN ({segment_times.index[segment_times.argmin()]})", encode_time(segment_times.min(), include_ns=False))
                    max_segment.metric(f"MAX ({segment_times.index[segment_times.argmax()]})", encode_time(segment_times.max(), include_ns=False))
                    mean_segment.metric("MEAN", encode_time(segment_times.mean(), include_ns=False))
                    median_segment.metric("MEDIAN", encode_time(segment_times.median(), include_ns=False))
                    std_segment.metric("STANDARD DEVIATION", f"{int(segment_times.std().total_seconds())} seconds")
                                        
         
            
            

        
