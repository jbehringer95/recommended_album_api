import React from "react";
import { Box, Chip } from "@mui/material";

const SelectedTags = ({ selected, onDelete }) => {
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
      }}
    >
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          flexWrap: "wrap",
          padding: "3% 0 0 0",
          width: "50vw",
        }}
      >
        {selected.map((val) => {
          return (
            <Chip
              key={val}
              label={val}
              variant="outlined"
              onDelete={() => onDelete(val)}
              sx={{
                backgroundColor: "#239E82",
                color: "white",
                margin: "5px 1%",
                border: "none",
              }}
            />
          );
        })}
      </Box>
    </Box>
  );
};

export default SelectedTags;
