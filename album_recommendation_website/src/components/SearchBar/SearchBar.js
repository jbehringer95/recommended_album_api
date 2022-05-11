import React from "react";
import { Box, Button } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import { useNavigate } from "react-router-dom";

const SearchBar = ({ searchHandler, selected }) => {
  const navigate = useNavigate();

  const onClickHandler = () => {
    const param = selected.join(", ");
    navigate(`/albums/${param}`);
  };
  return (
    <>
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          padding: "3% 0 0 0",
          width: "100vw",
        }}
      >
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            backgroundColor: "#dcdcdc",
            padding: "3px 10px",
            borderRadius: "8px",
            width: "40vw",
          }}
        >
          <input
            type="text"
            placeholder="Search here"
            onChange={searchHandler}
            style={{
              padding: "10px 5px",
              border: "none",
              width: "100%",
              outline: "none",
              backgroundColor: "#dcdcdc",
            }}
          />
          <SearchIcon />
        </Box>
        <Button
          disabled={selected.length === 0}
          sx={{
            ml: 2,
            borderRadius: "8px",
            backgroundColor: "#3e777b",
            "&:hover": {
              backgroundColor: "#3e777b",
            },
          }}
          variant="contained"
          onClick={onClickHandler}
        >
          Get Albums
        </Button>
      </Box>
    </>
  );
};

export default SearchBar;
