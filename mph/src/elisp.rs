use std::collections::HashMap;

use anyhow::{anyhow, Error, Result};
use nom::{
    branch::alt,
    bytes::complete::{escaped, tag},
    character::complete::{alphanumeric1, char, digit0, digit1, multispace0, one_of},
    combinator::{flat_map, map, map_res, opt},
    sequence::{delimited, pair, preceded, terminated, tuple},
    IResult,
};

#[derive(Debug)]
pub(crate) enum Exp {
    Nil,
    Integer(i64),
    Float(f64),
    Str(String),
    Symbol(String),
    Cons(Vec<Exp>),

    // Many of the data types that follow may be printed but not read. This
    // variant captures unreadable printed types not otherwise assigned to
    // a different type
    Unreadable(Option<String>, Option<String>),

    // A "general-purpose" array - very similar to a string but with arbitrary
    // expressions as values. They don't seem super useful for external
    // consumers.
    Vector(Vec<Exp>),

    // A hash table. Keys can, in actuality, be any expression!
    HashTable(HashMap<Exp, Exp>),

    // Various emacs types which are most likely unreadables.
    // TODO: Go through these types, print them w/ emacsclient, and update the
    // parser accordingly.
    Subr,
    ByteCodeFunction,
    Record,
    Buffer,
    Marker,
    Window,
    Frame,
    Process,
    Thread,
    Mutex,
    ConditionVariable,
    Stream,
    KeyMap,
    Overlay,
    Font,
}

fn nil(input: &str) -> IResult<&str, Exp> {
    let (input, _) = tag("nil")(input)?;
    Ok((input, Exp::Nil))
}

fn cons(input: &str) -> IResult<&str, Exp> {
    let mut parser = delimited(tag("("), multispace0, tag(")"));

    let (input, _) = parser(input)?;

    Ok((input, Exp::Nil))
}

fn integer_10(input: &str) -> IResult<&str, Exp> {
    map_res(
        pair(opt(one_of("+-")), terminated(digit1, opt(tag(".")))),
        |result| -> Result<Exp, Error> {
            let sgn = if let Some(s) = result.0 {
                s.to_string()
            } else {
                "".to_string()
            };

            let n = String::from(format!("{}{}", sgn, result.1)).parse::<i64>()?;
            Ok(Exp::Integer(n))
        },
    )(input)
}

fn radix(input: &str) -> IResult<&str, u32> {
    preceded(
        tag("#"),
        alt((
            map_res(one_of("box"), |radix| match radix {
                'b' => Ok(2),
                'o' => Ok(8),
                'x' => Ok(16),
                _ => Err(anyhow!("unknown radix: {}", radix)),
            }),
            map_res(
                terminated(digit1, tag("r")),
                |radix: &str| -> Result<u32, Error> {
                    println!("{}", radix);
                    let r = radix.parse()?;
                    Ok(r)
                },
            ),
        )),
    )(input)
}

fn integer_radix(input: &str) -> IResult<&str, Exp> {
    map_res(
        tuple((
            radix,
            opt(one_of("+-")),
            terminated(alphanumeric1, opt(tag("."))),
        )),
        |result| -> Result<Exp, Error> {
            let sgn = if let Some(s) = result.1 {
                s.to_string()
            } else {
                "".to_string()
            };

            let n = i64::from_str_radix(format!("{}{}", sgn, result.2).as_str(), result.0)?;
            Ok(Exp::Integer(n))
        },
    )(input)
}

fn integer(input: &str) -> IResult<&str, Exp> {
    alt((integer_radix, integer_10))(input)
}

fn float(input: &str) -> IResult<&str, Exp> {
    map_res(
        pair(
            opt(one_of("+-")),
            pair(
                pair(terminated(digit0, opt(tag("."))), digit0),
                opt(preceded(one_of("eE"), pair(opt(one_of("-+")), digit1))),
            ),
        ),
        |result| -> Result<Exp, Error> {
            let sgn = if let Some(s) = result.0 {
                s.to_string()
            } else {
                "".to_string()
            };

            let fmt = String::from(match result.1 {
                ((whole, fraction), Some(exp)) => {
                    let exp_sgn = if let Some(s) = exp.0 {
                        s.to_string()
                    } else {
                        "".to_string()
                    };
                    format!("{}{}.{}e{}{}", sgn, whole, fraction, exp_sgn, exp.1)
                }
                ((whole, fraction), None) => format!("{}{}.{}", sgn, whole, fraction),
            });

            let n = fmt.parse::<f64>()?;
            Ok(Exp::Float(n))
        },
    )(input)
}

fn string(input: &str) -> IResult<&str, Exp> {
    unimplemented!("string");
}

fn symbol(input: &str) -> IResult<&str, Exp> {
    unimplemented!("symbol");
}

#[cfg(test)]
mod tests {
    use anyhow::{Error, Result};

    use crate::elisp::{cons, float, integer, nil, string, symbol, Exp};

    #[test]
    fn parse_nil_symbol() -> Result<(), Error> {
        assert!(matches!(nil("nil")?, ("", Exp::Nil)));
        Ok(())
    }

    #[test]
    fn parse_nil_cons() -> Result<(), Error> {
        assert!(matches!(cons("()")?, ("", Exp::Nil)));
        Ok(())
    }

    #[test]
    fn parse_integer_simple() -> Result<(), Error> {
        assert!(matches!(integer("12345")?, ("", Exp::Integer(12345))));
        Ok(())
    }

    #[test]
    fn parse_integer_decimal_point() -> Result<(), Error> {
        assert!(matches!(integer("1.")?, ("", Exp::Integer(1))));
        Ok(())
    }

    #[test]
    fn parse_integer_positive() -> Result<(), Error> {
        assert!(matches!(integer("+1")?, ("", Exp::Integer(1))));
        Ok(())
    }

    #[test]
    fn parse_integer_negative() -> Result<(), Error> {
        assert!(matches!(integer("-1")?, ("", Exp::Integer(-1))));
        Ok(())
    }

    #[test]
    fn parse_integer_minus_zero() -> Result<(), Error> {
        assert!(matches!(integer("-0")?, ("", Exp::Integer(0))));
        Ok(())
    }

    #[test]
    fn parse_integer_binary() -> Result<(), Error> {
        assert!(matches!(integer("#b101100")?, ("", Exp::Integer(44))));
        Ok(())
    }

    #[test]
    fn parse_integer_octal() -> Result<(), Error> {
        assert!(matches!(integer("#o54")?, ("", Exp::Integer(44))));
        Ok(())
    }

    #[test]
    fn parse_integer_hex() -> Result<(), Error> {
        assert!(matches!(integer("#o54")?, ("", Exp::Integer(44))));
        Ok(())
    }

    #[test]
    fn parse_integer_radix() -> Result<(), Error> {
        assert!(matches!(integer("#24r1k")?, ("", Exp::Integer(44))));
        Ok(())
    }

    #[test]
    fn parse_float_simple() -> Result<(), Error> {
        assert!(matches!(float("1500.0")?, ("", Exp::Float(_))));
        Ok(())
    }

    #[test]
    fn parse_float_e2() -> Result<(), Error> {
        assert!(matches!(float("15e2")?, ("", Exp::Float(_))));
        Ok(())
    }

    #[test]
    fn parse_float_ep2() -> Result<(), Error> {
        assert!(matches!(float("15e+2")?, ("", Exp::Float(_))));
        Ok(())
    }

    #[test]
    fn parse_float_em3() -> Result<(), Error> {
        assert!(matches!(float("1500000e-3")?, ("", Exp::Float(_))));
        Ok(())
    }

    #[test]
    fn parse_float_point_e4() -> Result<(), Error> {
        assert!(matches!(float(".15e4")?, ("", Exp::Float(_))));
        Ok(())
    }

    #[test]
    fn parse_string_simple() -> Result<(), Error> {
        let res = string("\"abc\"")?;
        assert_eq!(res.0, "");
        assert!(matches!(res.1, Exp::Str(_)));
        if let Exp::Str(st) = res.1 {
            assert_eq!(st, "abc".to_string());
        }
        Ok(())
    }

    #[test]
    fn parse_string_escaped_quotes() -> Result<(), Error> {
        let res = string("\"abc\\\"1\\\"23\"")?;
        assert_eq!(res.0, "");
        assert!(matches!(res.1, Exp::Str(_)));
        if let Exp::Str(st) = res.1 {
            assert_eq!(st, "abc\"1\"23".to_string());
        }
        Ok(())
    }

    #[test]
    fn parse_string_escaped_backslash() -> Result<(), Error> {
        let res = string("\"abc\\\\123\"")?;
        assert_eq!(res.0, "");
        assert!(matches!(res.1, Exp::Str(_)));
        if let Exp::Str(st) = res.1 {
            assert_eq!(st, "abc\\123".to_string());
        }
        Ok(())
    }

    #[test]
    fn parse_string_newline() -> Result<(), Error> {
        let res = string(
            "\"abc
123\"",
        )?;
        assert_eq!(res.0, "");
        assert!(matches!(res.1, Exp::Str(_)));
        if let Exp::Str(st) = res.1 {
            assert_eq!(
                st,
                "abc
123"
                .to_string()
            );
        }
        Ok(())
    }

    #[test]
    fn parse_string_escaped_newline() -> Result<(), Error> {
        let res = string(
            "\"abc\\
123\"",
        )?;
        assert_eq!(res.0, "");
        assert!(matches!(res.1, Exp::Str(_)));
        if let Exp::Str(st) = res.1 {
            assert_eq!(st, "abc123".to_string());
        }
        Ok(())
    }

    #[test]
    fn parse_symbol_foo() -> Result<(), Error> {
        let res = symbol("foo")?;
        assert_eq!(res.0, "");
        assert!(matches!(res.1, Exp::Symbol(_)));
        if let Exp::Symbol(sym) = res.1 {
            assert_eq!(sym, "foo".to_string());
        }
        Ok(())
    }

    #[test]
    fn parse_symbol_foo_shouted() -> Result<(), Error> {
        let res = symbol("FOO")?;
        assert_eq!(res.0, "");
        assert!(matches!(res.1, Exp::Symbol(_)));
        if let Exp::Symbol(sym) = res.1 {
            assert_eq!(sym, "FOO".to_string());
        }
        Ok(())
    }

    #[test]
    fn parse_symbol_oneplus() -> Result<(), Error> {
        let res = symbol("1+")?;
        assert_eq!(res.0, "");
        assert!(matches!(res.1, Exp::Symbol(_)));
        if let Exp::Symbol(sym) = res.1 {
            assert_eq!(sym, "1+".to_string());
        }
        Ok(())
    }

    #[test]
    fn parse_symbol_plusone() -> Result<(), Error> {
        let res = symbol("\\+1")?;
        assert_eq!(res.0, "");
        assert!(matches!(res.1, Exp::Symbol(_)));
        if let Exp::Symbol(sym) = res.1 {
            assert_eq!(sym, "+1".to_string());
        }
        Ok(())
    }

    #[test]
    fn parse_symbol_nasty() -> Result<(), Error> {
        let res = symbol("+-*/_~!@$%^&=:<>{}")?;
        assert_eq!(res.0, "");
        assert!(matches!(res.1, Exp::Symbol(_)));
        if let Exp::Symbol(sym) = res.1 {
            assert_eq!(sym, "'+-*/_~!@$%^&=:<>{}".to_string());
        }
        Ok(())
    }
}
