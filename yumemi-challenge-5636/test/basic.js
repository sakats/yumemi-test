const codecheck = require("codecheck");

const language = process.env.CHALLENGE_LANGUAGE || "ja";
const appCommand = process.env.APP_COMMAND;
 
const settings = require("./settings.json");
settings.language = language;
const testcases = require("./basic_testcases.json");
 
const testRunner = codecheck.testRunner(settings, appCommand);

const {assert} = require("chai");

// add for non 0 exit.
const MESSAGES = {
    'ja': {
        ERROR_ZERO_STATUS_CODE: 'ステータスコードが異常終了 (0 以外) ではありません'
    },
    'en': {
        ERROR_ZERO_STATUS_CODE: 'Exit status should not be 0.'
    }
}[language];

testRunner.verifyStatusCode = async function(testcase, inputData, outputData, result) {
    const MSG = this.messageBuilder;
    const shouldError = testcase._json.output.type === "error";

    if (shouldError) {
        testcase._output = "test/out/basic/empty.out";
    }
    if (shouldError !== (result.code === 0)) {
        return;
    } else if (shouldError) {
        console.log(await MSG.abnormalEnd(inputData, outputData, result));
        assert.fail(await MSG.msg.format(MESSAGES.ERROR_ZERO_STATUS_CODE));
    } else {
        console.log(await MSG.abnormalEnd(inputData, outputData, result));
        assert.fail(await MSG.nonZeroStatusCode());
    }
};

testRunner.runAll(testcases);
