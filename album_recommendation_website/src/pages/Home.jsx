import { Box, Typography } from "@mui/material";
import Footer from "./Footer";
import { fetchTags } from "../api/api";
import { useEffect, useState } from "react";
import { SearchBar, SelectedTags, SearchResults } from "../components";

const HomePage = () => {
  const [tags, setTags] = useState([]);
  const [filteredTags, setFilteredtags] = useState([]);
  const [selected, setSelected] = useState([]);

  //set Selected Chip
  const chipHandler = (val, i) => {
    setSelected((preVal) => [...preVal, val]);
  };

  //Search handler
  const searchHandler = (search) => {
    search = search.replace(/\s+/g, " ").trim();
    if (search === "") {
      return setFilteredtags([]);
    }
    const filteredTags = tags
      .filter((tag) => {
        return tag.toLowerCase().includes(search.toLowerCase());
      })
      .slice(0, 10);

    setFilteredtags(filteredTags);
  };

  //Delete Selected Chip
  const onDelete = (val) => {
    setSelected((preVal) => preVal.filter((tag) => tag !== val));
  };

  //fetches tags from API
  useEffect(() => {
    async function getTags() {
      try {
        const tagResponse = await fetchTags();
        if (tagResponse) setTags(tagResponse);
      } catch (error) {
        console.log("Error occur");
      }
    }
    getTags();
  }, []);

  return (
    <Box>
      <Box sx={{ marginTop: "20px" }}>
        <Typography variant="h2" sx={{ textAlign: "center", color: "white" }}>
          Search Albums
        </Typography>
      </Box>
      <SelectedTags selected={selected} onDelete={onDelete} />
      <SearchBar
        searchHandler={(e) => searchHandler(e.target.value)}
        selected={selected}
      />
      <SearchResults
        filteredTags={filteredTags}
        selected={selected}
        chipHandler={chipHandler}
      />
      <Footer />
    </Box>
  );
};

export default HomePage;
