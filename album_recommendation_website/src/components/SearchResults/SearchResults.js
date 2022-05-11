import React from "react";
import { Box, Chip } from "@mui/material";

const SearchResults = ({ filteredTags, selected, chipHandler }) => {
  const styles = {
    chipNotSelected: {
      backgroundColor: "#239E82",
      color: "white",
      margin: "10px 1%",
      border: "none",
    },
    chipSelected: {
      backgroundColor: "#116955",
      color: "white",
      margin: "10px 1%",
      border: "none",
    },
  };

  return (
    <>
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          mb: 4,
        }}
      >
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            flexWrap: "wrap",
            padding: "3% 0 0 0",
            width: { xs: "80vw", sm: "55vw" },
          }}
        >
          {filteredTags.map((val, i) => {
            return (
              <Chip
                key={i}
                label={val}
                disabled={selected.some((item) => item === val)}
                variant="outlined"
                onClick={() => chipHandler(val, i)}
                sx={
                  selected.some((item) => item === val)
                    ? styles.chipSelected
                    : styles.chipNotSelected
                }
              />
            );
          })}
        </Box>
      </Box>
    </>
  );
};

export default SearchResults;
