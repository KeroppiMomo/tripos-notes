const preamble = `
{{preamble}}
`

MathJax = {
    tex: {
        inlineMath: [['$', '$']],
        displayMath: [['$$', '$$']],
    },
    startup: {
        ready: () => {
            MathJax.startup.defaultReady();
            MathJax.tex2chtml(preamble);

            const unicodeRanges = MathJax._.core.MmlTree.OperatorDictionary.RANGES;
            unicodeRanges[4][0] = 0x03AC;
            unicodeRanges.splice(4, 0, [880, 940, 0, "mo"]);
        },
    },
};
