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
        },
    },
};
