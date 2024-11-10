import { ChakraProvider } from '@chakra-ui/react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import {
  createBrowserRouter,
  RouterProvider} from "react-router-dom";
import PersonPage from './components/PersonPage/PersonPage.tsx'
import AuthPage from './components/LoginPage/Login.tsx'
import { createContext } from 'react';
import Store from './store/store.ts';
//ts-ignore
import HRPage from './components/HRPage/HRPage.tsx';

const store = new Store();
export const Context = createContext({
    store,
})


const router = createBrowserRouter([
  {
    path: "/",
    element: <App/>,
  },
  {
    path: "/person",
    element: <PersonPage/>,
  },
  {
    path: "/login",
    element: <AuthPage/>
  },
  {
    path: "/hr",
    element: <HRPage/>,
  }
]);

createRoot(document.getElementById('root')!).render(
  <Context.Provider value={{store}}>
  <ChakraProvider>
    <RouterProvider router={router} />
  </ChakraProvider>
</Context.Provider>
)
