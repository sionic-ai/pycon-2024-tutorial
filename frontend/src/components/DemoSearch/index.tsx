import { Box, Button, Text } from "@mantine/core";
import classes from "./DemoSearch.module.css";
import { IconPointerSearch } from "@tabler/icons-react";

type DemoSearchProps = {
    handleDemoSearch: (query: string) => void;
};

export default function DemoSearch({ handleDemoSearch }: DemoSearchProps) {


  return (
    <Box className={classes.wrapper}>
      <Text
      className={classes.demoText}
      >Try this:</Text>
      <Button
        variant="outline"
        leftSection={<IconPointerSearch size={"1.3rem"} />}
        className={classes.demoBtn}
        onClick={() => handleDemoSearch("main 실행하는 코드 알려주세요.")}
      >
        main 실행하는 코드 알려주세요.
      </Button>
      <Button
        variant="outline"
        leftSection={<IconPointerSearch  size={"1.3rem"}/>}
        className={classes.demoBtn}
        onClick={() => handleDemoSearch("승자를 맞추는 코드는 어디에 있나요?")}
      >
        승자를 맞추는 코드는 어디에 있나요?
      </Button>
      <Button
        variant="outline"
        leftSection={<IconPointerSearch  size={"1.3rem"}/>}
        className={classes.demoBtn}
        onClick={() => handleDemoSearch("자동차를 만드는 코드는 어디에 있나요?")}
      >
        자동차를 만드는 코드는 어디에 있나요?
      </Button>
    </Box>
  );
}
