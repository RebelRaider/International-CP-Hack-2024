import { Box, Button, Heading, Text, Image, Flex } from '@chakra-ui/react'
import './App.css'
import Header from './components/Header/Header'
import Layout from './Layout'
import { Link } from 'react-router-dom'

function App() {
  return (
    <Layout>
      <Header />
      {/* Первая страница */}
      <Box p={8} marginTop={10}>
        <Flex alignItems="center" justifyContent="space-between">
          <Box flex="1" mr={8}>
            <Heading as="h1" size="2xl" mb={4}>
            Узнайте личностные качества с помощью OCEAN и MBTI
            </Heading>
            <Text fontSize="lg">
            Наше решение позволяет анализировать тип личности с помощью видеовизитки, резюме и мотивационного письма. Понимание личностного типа помогает глубже узнать ваши сильные стороны и определить предпочтения в рабочей среде.
            </Text>
            <Button colorScheme="blue" marginTop={5} 
            as={Link}
        to="/person">Пройти оценку</Button>
          </Box>
          <Image
            flex="1"
            src="/man2.svg"
            alt="Пример изображения"
            borderRadius="lg"
            w={400}
          />
        </Flex>
      </Box>
      <Box p={8} >
        <Flex alignItems="center" justifyContent="space-between">
          <Image
            flex="1"
            src="/woman2.svg"
            alt="Пример изображения"
            borderRadius="lg"
            mr={8}
            w={400}
          />
          <Box flex="1">
            <Heading as="h1" size="2xl" mb={4}>
            Подберите сотрудника по вашим потребностям
            </Heading>
            <Text fontSize="lg" mb={4}>
            Наше решение помогает HR-специалистам легко находить сотрудников, чьи личные качества и профессиональные навыки максимально подходят для вакансий. С помощью анализа личности и рекомендаций, мы делаем процесс найма более целевым и эффективным, что помогает находить людей, идеально подходящих под культуру и требования вашей компании.
            </Text>
            <Button colorScheme="orange" as={Link}
        to="/login">Подобрать сотрудника</Button>
          </Box>
        </Flex>
      </Box>
    </Layout>
  )
}

export default App
