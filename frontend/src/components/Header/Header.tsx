import { Box, Button } from "@chakra-ui/react";
import { Link, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";

const Header = () => {
  const location = useLocation();
  const [scrollY, setScrollY] = useState(0);

  const isActive = (path: string): boolean => location.pathname === path;

  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <Box
      display="flex"
      justifyContent="space-between"
      p={4}
      bg={`rgba(253, 253, 253, ${Math.max(1 - scrollY / 200, 0.7)})`}
      borderBottomRadius={30}
      zIndex={1000}
      position="fixed"
      w="65%"
      transition="background-color 0.3s ease"
    >
      <Button
        as={Link}
        to="/"
        colorScheme={isActive("/") ? "blue" : "gray"}
        variant={isActive("/") ? "solid" : "ghost"}
      >
        Главная
      </Button>

      <Box display="flex">
        <Button
          as={Link}
          to="/person"
          colorScheme={isActive("/person") ? "blue" : "gray"}
          variant={isActive("/person") ? "solid" : "ghost"}
          mx={2}
        >
          Персональная
        </Button>
        
        <Button
          as={Link}
          to="/login"
          colorScheme={isActive("/hr") ? "blue" : "gray"}
          variant={isActive("/hr") ? "solid" : "ghost"}
          mx={2}
        >
          HR
        </Button>
      </Box>
    </Box>
  );
};

export default Header;
