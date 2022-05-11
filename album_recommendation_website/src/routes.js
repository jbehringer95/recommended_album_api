import { useRoutes } from "react-router-dom";
import Home from "./pages/Home";
import AlbumDetails from "./pages/AlbumDetails";

const AppRouter = () => {
  let element = useRoutes([
    { path: "/", element: <Home /> },
    { path: "/albums/:albumQuery", element: <AlbumDetails /> },
  ]);

  return element;
};

export default AppRouter;
