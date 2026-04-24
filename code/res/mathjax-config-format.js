const preamble = `
{{preamble}}
`

MathJax = {
    loader: {
        load: [
            '[tex]/extpfeil',
            '[tex]/mathtools',
        ],
    },
    tex: {
        inlineMath: [['$', '$']],
        displayMath: [['$$', '$$']],
        extensions: ["extpfeil.js"],
        packages: {'[+]': [
            'mathtools',
            'extpfeil',
        ]},
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
