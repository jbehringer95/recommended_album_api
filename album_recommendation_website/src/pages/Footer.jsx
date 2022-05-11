import { Typography } from "@mui/material";
import { Box } from "@mui/system";

const Footer = () => {
  return (
    <Box
      sx={{
        width: "100vw",
        textAlign: "center",
        padding: "20px 0",
        position: "fixed",
        bottom: "0px",
        backgroundColor: "#353b43",
        overflowX: "hidden",
      }}
    >
      <Typography sx={{ color: "white", fontSize: "16px" }}>
        Trademark Info
      </Typography>
    </Box>
  );
};

export default Footer;
