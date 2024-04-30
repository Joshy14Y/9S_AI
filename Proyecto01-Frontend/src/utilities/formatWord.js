export const formatWord = (word) => {
    // Remove whitespaces and symbols using a regular expression
    let cleanWord = word.replace(/[\W_]/g, '');
    // Convert the word to lowercase
    cleanWord = cleanWord.toLowerCase();

    return cleanWord;
}