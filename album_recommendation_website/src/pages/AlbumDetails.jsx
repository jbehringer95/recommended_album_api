import { fetchRecommendedAlbum } from "../api/api";
import { useEffect, useState } from "react";
import { Box } from "@mui/system";
import { useParams } from "react-router-dom";
import { Typography, Button } from "@mui/material";
import Footer from "./Footer";

const AlbumDetails = () => {
  let { albumQuery } = useParams();
  const searchQuery = encodeURI(`[${albumQuery}]`);

  const [albums, setAlbum] = useState(null);
  const [index, setindex] = useState(0);

  function nextAlbum() {
    if (index < albums.length - 1) {
      setindex(index + 1);
    }
  }
  function prevAlbum() {
    if (index > 0) {
      setindex(index - 1);
    }
  }

  useEffect(() => {
    async function getAlbum() {
      try {
        const albumResponse = await fetchRecommendedAlbum({ searchQuery });
        if (albumResponse) setAlbum(albumResponse);
        else setAlbum([]);
      } catch (error) {
        console.log("Error occur");
      }
    }
    getAlbum();
  }, [searchQuery]);
  return (
    <Box>
      {albums?.length ? (
        <Box sx={{ padding: "3% 8%" }}>
          <Box sx={{ display: "flex", justifyContent: "center" }}>
            <Box
              sx={{
                display: "flex",
                justifyContent: "center",
                maxWidth: "250px",
              }}
            >
              <img
                width="100%"
                height="auto"
                src={albums?.length ? albums[index].url : null}
                alt={albums?.length ? albums[index].url : null}
              />
            </Box>
          </Box>
          <Box
            sx={{
              marginTop: "20px",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              flexDirection: "column",
            }}
          >
            <Typography
              variant="h5"
              sx={{ textAlign: "center", color: "white" }}
            >
              {albums?.length ? albums[index].Album_Name : null}
            </Typography>
            <Box
              sx={{
                color: "white",
                width: { sm: "70vw", md: "50vw" },
                display: "flex",
                justifyContent: "center",
                alignItems: "start",
                flexDirection: "column",
              }}
            >
              {/* Artist */}
              <Box
                sx={{
                  display: "flex",
                  mt: 2,
                }}
              >
                <Typography variant="h6">Artist:</Typography>
                <Box sx={{ textAlign: "left", ml: 12, color: "#c7cdc1" }}>
                  <Typography variant="h6">
                    {albums?.length ? albums[index].Artist : null}{" "}
                  </Typography>
                </Box>
              </Box>
              {/* Genres */}
              <Box
                sx={{
                  display: "flex",
                  mt: 2,
                }}
              >
                <Typography variant="h6">Genres:</Typography>
                <Box sx={{ textAlign: "left", ml: 10, color: "#c7cdc1" }}>
                  <Typography variant="h6">
                    {" "}
                    {albums?.length ? albums[index].Genres : null}{" "}
                  </Typography>
                  <Typography variant="body2">
                    {" "}
                    {albums?.length ? albums[index].Sec_Genres : null}{" "}
                  </Typography>
                </Box>
              </Box>
              <Box
                sx={{
                  display: "flex",
                  mt: 2,
                }}
              >
                {/* Descriptors */}
                <Typography variant="h6">Descriptors:</Typography>
                <Box sx={{ textAlign: "left", ml: 4, color: "#c7cdc1" }}>
                  <Typography variant="h6">
                    {" "}
                    {albums?.length ? albums[index].Descriptors : null}{" "}
                  </Typography>
                </Box>
              </Box>
            </Box>
          </Box>
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-evenly",
              margin: "20px",
            }}
          >
            <Button
              variant="contained"
              sx={{
                backgroundColor: "#3e777b",
                "&:hover": {
                  backgroundColor: "#3e777b",
                },
              }}
              onClick={prevAlbum}
            >
              Previous
            </Button>
            <Button
              variant="contained"
              sx={{
                backgroundColor: "#3e777b",
                "&:hover": {
                  backgroundColor: "#3e777b",
                },
              }}
              onClick={nextAlbum}
            >
              Next
            </Button>
          </Box>
        </Box>
      ) : (
        <Box sx={{ marginTop: "20px" }}>
          <Typography variant="h5" sx={{ textAlign: "center", color: "white" }}>
            {!albums || albums === "undefined"
              ? "Loading..."
              : "No Album Found"}
          </Typography>
        </Box>
      )}
      <Footer />
    </Box>
  );
};

export default AlbumDetails;
