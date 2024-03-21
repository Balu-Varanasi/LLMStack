import { useParams } from "react-router-dom";
import Grid from "@mui/material/Unstable_Grid2";
import StoreApp from "../components/store/StoreApp";
import Search from "../components/store/Search";

export default function HomePage() {
  const { appSlug = "super-agent" } = useParams();

  return (
    <Grid container sx={{ height: "100%" }}>
      <Grid xs={12} md={7}>
        <StoreApp appSlug={appSlug} />
      </Grid>
      <Grid xs={12} md={5}>
        <Search appSlug={appSlug} />
      </Grid>
    </Grid>
  );
}
