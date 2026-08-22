import {
  createBrowserRouter,
  RouterProvider,
} from 'react-router';


const router = createBrowserRouter([
  // Define your routes here
]);

export const AppRouter = () => {
  return <RouterProvider router={router} />;
};