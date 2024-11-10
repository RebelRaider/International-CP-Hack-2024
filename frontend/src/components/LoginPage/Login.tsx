import  { useState } from 'react';
import { Box, Button, Input, VStack, Heading, Text, useToast } from '@chakra-ui/react';
import Store from '../../store/store.ts';

const store = new Store();

import { useEffect } from 'react';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const toast = useToast();

  const handleLogin = async () => {
    if (localStorage.getItem('token')) {
      window.location.href = '/hr';
      return;
    }
    try {
      await store.login(username, password);
      window.location.href = '/hr';
      toast({
        title: 'Login successful.',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (e) {
      toast({
        title: 'Login failed.',
        description: 'Please check your credentials and try again.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <Box p={6} boxShadow="lg" maxW="md" m="auto" mt={10}>
      <VStack spacing={4}>
        <Heading size="lg">Login</Heading>
        <Input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <Input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button colorScheme="blue" onClick={handleLogin} isLoading={store.isLoading}>
          Login
        </Button>
      </VStack>
    </Box>
  );
};

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const toast = useToast();

  const handleRegister = async () => {
    try {
      await store.registration(username, password);
      toast({
        title: 'Регистрация прошла успешно.',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      setTimeout(() => {
         window.location.href = '/login'
      }, 3000);
    } catch (e) {
      toast({
        title: 'Повторите попытку',
        description: 'Проверьте введенные данные и попробуйте снова.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <Box p={6} boxShadow="lg" maxW="md" m="auto" mt={10}>
      <VStack spacing={4}>
        <Heading size="lg">Register</Heading>
        <Input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <Input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button colorScheme="teal" onClick={handleRegister}>
          Register
        </Button>
      </VStack>
    </Box>
  );
};

const AuthPage = () => {
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    if (localStorage.getItem('token')) {
      window.location.href = '/hr';
    } else {
      setLoading(false);
    }
  }, []);
  useEffect(() => {
    if (localStorage.getItem('token')) {
      window.location.href = '/hr';
    }
  }, []);
  const [isLoginPage, setIsLoginPage] = useState(true);

  if (loading) {
    return (
      <Box textAlign="center" mt={10}>
        <Text>Loading...</Text>
      </Box>
    );
  }


  return (
    <Box>
      {isLoginPage ? <Login /> : <Register />}
      <Box textAlign="center" mt={4}>
        <Text>
          {isLoginPage ? "Don't have an account?" : 'Already have an account?'}
          <Button variant="link" ml={2} onClick={() => setIsLoginPage(!isLoginPage)}>
            {isLoginPage ? 'Register here' : 'Login here'}
          </Button>
        </Text>
      </Box>
    </Box>
  );
};

export default AuthPage;
