import { useEffect, useState } from "react";
import {
  Box,
  Chip,
  CircularProgress,
  InputBase,
  IconButton,
  Paper,
  Typography,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import capitalize from "lodash/capitalize";
import { useRecoilValue } from "recoil";
import { axios } from "../../data/axios";
import {
  appsByStoreCategoryState,
  storeCategoriesSlugState,
} from "../../data/atoms";

function AppEntry({ app }) {
  return (
    <Box
      sx={{
        border: "1px solid #e0e0e0",
        borderRadius: "4px",
        backgroundColor: "#f8f8f8",
        p: 1,
        m: 1,
        display: "flex",
        alignItems: "center",
        cursor: "pointer",
        textAlign: "left",
        ":hover": {
          backgroundColor: "#edeff7",
          borderColor: "#d0d0d0",
          borderRadius: "4px",
          boxShadow: "0 0 0 1px #d0d0d0",
        },
      }}
      onClick={() => {
        window.location.href = `/a/${app.slug}`;
      }}
    >
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          textAlign: "left",
          pl: 1,
          pb: 1,
        }}
      >
        <img
          src={app.icon128}
          alt={app.name}
          style={{
            width: 70,
            height: 70,
            margin: "1em 0.5em",
            borderRadius: "0.2em",
            alignSelf: "start",
          }}
        />
        <Box sx={{ padding: 2 }}>
          <Typography
            component="div"
            color="text.primary"
            sx={{ fontSize: 18, fontWeight: 600 }}
          >
            {app.name}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {app.description?.length > 200
              ? `${app.description.substring(0, 200)}...`
              : app.description}
          </Typography>
          <Box sx={{ mt: 1, mb: 1 }}>
            {app.categories &&
              app.categories.map((category) => (
                <Chip
                  label={capitalize(category)}
                  size="small"
                  key={category}
                />
              ))}
          </Box>
        </Box>
      </Box>
    </Box>
  );
}

export default function Search({ appSlug }) {
  const [categoryFilter, setCategoryFilter] = useState(
    appSlug ? "recommended" : "featured",
  );
  const defaultCategories = useRecoilValue(storeCategoriesSlugState);
  const [appCategories, setAppCategories] = useState(defaultCategories);
  const [searchTerm, setSearchTerm] = useState("");
  const [searching, setSearching] = useState(false);
  const [apps, setApps] = useState([]);
  const appsByStoreCategory = useRecoilValue(
    appsByStoreCategoryState(
      categoryFilter.toLowerCase().startsWith("recommended")
        ? `recommended/${appSlug}`
        : categoryFilter.toLowerCase(),
    ),
  );

  useEffect(() => {
    if (categoryFilter && searchTerm === "") {
      setApps(appsByStoreCategory);
      setAppCategories(defaultCategories);
    }
  }, [appsByStoreCategory, defaultCategories, searchTerm, categoryFilter]);

  const searchApps = (term) => {
    setSearching(true);
    if (term === "") {
      setApps(appsByStoreCategory);
      setAppCategories(defaultCategories);
      setSearching(false);
    } else {
      axios()
        .get(`/api/store/search?query=${term}`)
        .then((response) => {
          setApps(response.data?.results || []);

          const categories = response.data?.results
            ?.map((app) => app?.categories)
            .flat();
          setAppCategories([...new Set(categories)]);
        })
        .catch((error) => {
          console.error(error);
        })
        .finally(() => {
          setSearching(false);
        });
    }
  };

  return (
    <Box
      ml={2}
      mr={2}
      pt={1}
      sx={{ display: "flex", flexDirection: "column", maxHeight: "100vh" }}
    >
      <Paper
        component="form"
        sx={{ p: "2px 4px", display: "flex", alignItems: "center" }}
        onSubmit={(e) => {
          e.preventDefault();
          searchApps(searchTerm);
        }}
      >
        <InputBase
          sx={{ ml: 1, flex: 1 }}
          placeholder="Explore Promptly Apps"
          inputProps={{ "aria-label": "Explore Promptly Apps" }}
          value={searchTerm}
          onChange={(e) => {
            setSearchTerm(e.target.value);
          }}
        />
        <IconButton
          type="button"
          sx={{ p: "10px" }}
          aria-label="search"
          onClick={() => searchApps(searchTerm)}
        >
          <SearchIcon />
        </IconButton>
      </Paper>
      {searching && (
        <Box sx={{ textAlign: "center", mt: 2 }}>
          <CircularProgress />
        </Box>
      )}

      {!searching && (
        <>
          <Box sx={{ textAlign: "left", mt: 1 }}>
            {appCategories.map((category) => (
              <Chip
                key={category}
                label={capitalize(category)}
                size="small"
                variant={
                  categoryFilter.toLowerCase() === category.toLowerCase() ||
                  (categoryFilter.startsWith("recommended") &&
                    category.toLowerCase().startsWith("recommended"))
                    ? "filled"
                    : "outlined"
                }
                sx={{
                  cursor: "pointer",
                  m: 0.5,
                  border:
                    categoryFilter.toLowerCase() === category.toLowerCase()
                      ? "1px solid #b0b0b0"
                      : "1px solid #e0e0e0",
                }}
                onClick={() =>
                  setCategoryFilter(
                    category.toLowerCase().startsWith("recommended")
                      ? `recommended/${appSlug}`
                      : category.toLowerCase(),
                  )
                }
              />
            ))}
          </Box>
          {apps.length === 0 && (
            <Box sx={{ textAlign: "center", mt: 2 }}>
              <p>No apps found</p>
            </Box>
          )}
          <Box sx={{ overflowY: "auto", flex: "1 1 auto" }}>
            {apps.length > 0 &&
              apps.map((app) => <AppEntry app={app} key={app.slug} />)}
          </Box>
        </>
      )}
    </Box>
  );
}
