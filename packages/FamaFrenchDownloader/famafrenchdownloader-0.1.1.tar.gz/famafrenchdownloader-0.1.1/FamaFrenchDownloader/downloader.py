import requests
import zipfile
import io
import pandas as pd
import re

class FamaFrenchFactor:

    @classmethod
    def get_data(cls, annual=True, region="North_America", factors="5"):
        factors_str = str(factors).upper()

        if isinstance(region, list):
            all_dfs = []
            for r in region:
                df_single = cls.get_data(annual=annual, region=r, factors=factors_str)
                # Rinomina colonne: WML → Region_WML, ecc.
                renamed = {col: f"{r}_{col}" for col in df_single.columns}
                df_single.rename(columns=renamed, inplace=True)
                all_dfs.append(df_single)

            return pd.concat(all_dfs, axis=1)

        region = region.strip()
        FAMA_FRENCH_REGIONS = [
            "US", "North_America", "Europe", "Japan",
            "Asia_Pacific_ex_Japan", "Developed", "Developed_ex_US"
        ]
        FAMA_FRENCH_FACTORS = ["3", "5", "MOM"]

        if region not in FAMA_FRENCH_REGIONS:
            raise ValueError(f"Region '{region}' not supported. Choose from {FAMA_FRENCH_REGIONS}")
        if factors_str not in FAMA_FRENCH_FACTORS:
            raise ValueError(f"Factor '{factors}' not valid. Choose from {FAMA_FRENCH_FACTORS}")

        # Link dinamico
        if region == "US" and factors_str == "3":
            url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip"
        elif region == "US" and factors_str == "5":
            url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip"
        elif region == "US" and factors_str == "MOM":
            url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_CSV.zip"
        elif factors_str == "MOM":
            url = f"https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/{region}_Mom_Factor_CSV.zip"
        else:
            url = f"https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/{region}_{factors_str}_Factors_CSV.zip"

        response = requests.get(url)
        response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            filename = z.namelist()[0]
            with z.open(filename) as f:
                return cls._parse_csv(f, annual)

    @staticmethod
    def _parse_csv(file, annual):
        lines = [line.decode("latin1") if isinstance(line, bytes) else line for line in file]

        header_line_index = next(
            i for i, l in enumerate(lines) if re.search(r",\s*(Mkt-RF|WML|Mom)", l)
        )
        selected_lines = lines[header_line_index:]

        df = pd.read_csv(io.StringIO("".join(selected_lines)), index_col=0)
        df.columns = df.columns.str.strip()
        df.index = df.index.astype(str).str.strip()

        if annual:
            df = df[df.index.str.fullmatch(r"\d{4}")]
            df.index = pd.to_datetime(df.index, format="%Y") + pd.offsets.YearEnd(0)
        else:
            df = df[df.index.str.fullmatch(r"\d{6}")]
            df.index = pd.to_datetime(df.index, format="%Y%m")

        df = df.apply(pd.to_numeric, errors="coerce")
        df.dropna(how="all", inplace=True)

        if "Mom" in df.columns:
            df.rename(columns={"Mom": "WML"}, inplace=True)

        return df