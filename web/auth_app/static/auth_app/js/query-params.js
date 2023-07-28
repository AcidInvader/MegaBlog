console.log('query-param loads.....')
function getQueryParams() {
    let queryDict = {};
    const searchParams = new URLSearchParams(document.location.search)
    for (const [key, value] of searchParams.entries()) {
        queryDict[key] = value;
    }
    return queryDict
}