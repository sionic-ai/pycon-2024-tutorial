import {
  Container,
  Group,
  Button,
  Modal,
  Title,
  Text,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import classes from "./CustomHeader.module.css";
import { Logo } from "../Logo";
import { IconBrandGithub } from "@tabler/icons-react";

export function CustomHeader() {
  const [opened, handlers] = useDisclosure(false);

  return (
    <header className={classes.header}>
      <Container size="lg" className={classes.inner}>
        <Logo size={35} />
        <Group gap={5} wrap="nowrap">
          <Button
            color="Neutral.6"
            variant="subtle"
            className={classes.link}
            component="a"
            href="https://sionic.ai"
            target="_blank"
            rel="noopener noreferrer"
          >
            sionic.ai
          </Button>
          <Button
            color="Neutral.6"
            variant="subtle"
            className={classes.link}
            onClick={handlers.open}
          >
            About
          </Button>
          <Button
            color="Neutral.6"
            variant="subtle"
            className={classes.link}
            component="a"
            href="https://github.com/sionic-ai/pycon-2024-tutorial"
            target="_blank"
            rel="noopener noreferrer"
            leftSection={<IconBrandGithub size={20} />}
          >
            GitHub
          </Button>
        </Group>
      </Container>
      <Modal opened={opened} onClose={handlers.close} centered size={"lg"}>
        <Modal.Header
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Title className={classes.modalHeader}>
            How does{" "}
            <Text component="span" className={classes.highlight} inherit>
              Code search
            </Text>{" "}
            work?
          </Title>
          <Text className={classes.subHeading}>
            Rust로 만든 자동차 경주 게임을 시만틱 검색으로 찾아보는 예제 앱입니다.
          </Text>
        </Modal.Header>
        <Modal.Body
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Text size="lg" color="dimmed" className={classes.description}>
            코드베이스를 검색할 때, 다음과 같은 목적이 있을 수 있습니다:
            현재 사용 중인 코드와 유사한 코드 스니펫을 찾거나, <b>특정 기능</b>을 수행하는
            메서드를 찾는 것입니다.
          </Text>
          <Text size="lg" color="dimmed" className={classes.description}>
            임베딩을 모두 활용하면 관련 메서드뿐만 아니라 그 안의 코드 조각까지 찾을 수 있습니다.
          </Text>
          <Button
            className={classes.modalBtnInner}
            radius={30}
            size={"md"}
            variant="filled"
            color="Primary.2"
            onClick={handlers.close}
          >
            Get started
          </Button>
        </Modal.Body>
      </Modal>
    </header>
  );
}
