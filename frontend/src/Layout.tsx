import { Box } from "@chakra-ui/react";


interface LayoutProps {
    children: React.ReactNode;
  }


const Layout: React.FC<LayoutProps> = ({ children}) => {
  return (
    <Box
      display="flex"
      justifyContent="center"
      minHeight="100vh"
      bg="gray.50"
    >
      <Box width="80%" maxWidth="1200px" >
        {children}
      </Box>
    </Box>
  );
};

export default Layout;